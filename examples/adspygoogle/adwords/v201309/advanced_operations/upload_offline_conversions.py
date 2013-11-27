#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Imports offline conversion values for specific clicks into your account.

To get THE Google Click ID for a click, run a CLICK_PERFORMANCE_REPORT.

Tags: ConversionTrackerService.mutate, OfflineConversionFeedService.mutate
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


conversion_name = 'INSERT_CONVERSION_NAME_HERE'
# Your click ID must be less than 30 days old.
click_id = 'INSERT_GOOGLE_CLICK_ID_HERE'
# The conversion time must be more recent than the time of the click.
conversion_time = 'INSERT_CONVERSION_TIME_HERE'
conversion_value = 'INSERT_CONVERSION_VALUE_HERE'


def main(client, conversion_name, click_id, conversion_time, conversion_value):
  # Initialize appropriate services.
  conversion_tracker_service = client.GetConversionTrackerService(
      version='v201309')

  offline_conversion_feed_service = client.GetOfflineConversionFeedService(
      version='v201309')

  # Once created, this entry will be visible under
  # Tools and Analysis->Conversion and will have "Source = Import".
  upload_conversion = {
      'xsi_type': 'UploadConversion',
      'category': 'PAGE_VIEW',
      'name': conversion_name,
      'viewthroughLookbackWindow': '30',
      'ctcLookbackWindow': '90'
  }

  upload_conversion_operation = {
      'operator': 'ADD',
      'operand': upload_conversion
  }

  response = conversion_tracker_service.mutate([upload_conversion_operation])[0]
  new_upload_conversion = response['value'][0]

  print ('New upload conversion type with name \'%s\' and ID \'%s\' was '
         'created.' % (new_upload_conversion['name'],
                       new_upload_conversion['id']))

  # Associate offline conversions with the upload conversion we created.
  feed = {
      'conversionName': conversion_name,
      'conversionTime': conversion_time,
      'conversionValue': conversion_value,
      'googleClickId': click_id
  }

  offline_conversion_operation = {
      'operator': 'ADD',
      'operand': feed
  }

  offline_conversion_response = offline_conversion_feed_service.mutate(
      [offline_conversion_operation])[0]
  new_feed = offline_conversion_response['value'][0]

  print ('Uploaded offline conversion value of \'%s\' for Google Click ID '
         '\'%s\' to \'%s\'.' % (new_feed['conversionValue'],
                                new_feed['googleClickId'],
                                new_feed['conversionName']))


if __name__ == '__main__':
  # Initialize client object.
  client_ = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client_, conversion_name, click_id, conversion_time, conversion_value)
