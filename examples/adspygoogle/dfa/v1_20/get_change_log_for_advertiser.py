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

"""This example displays the change logs of a specified advertiser object.
Results are limited to the first 10 records.

A similar pattern can be applied to get change logs for many other object
types. Run GetChangeLogObjectTypes.java for a list of other supported object
types and their ID numbers.

Tags: changelog.getChangeLogRecords
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


ADVERTISER_ID = 'INSERT_ADVERTISER_ID_HERE'


def main(client, advertiser_id):
  # Initialize appropriate service.
  change_log_service = client.GetChangeLogService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Create change log search criteria structure.
  change_log_search_criteria = {
      'pageSize': '10',
      'objectId': advertiser_id,
      # The following field has been filled in to choose advertiser change
      # logs. This values was determined using get_change_log_object_types.py.
      'objectTypeId': '1'
  }

  # Get change log record set.
  results = change_log_service.GetChangeLogRecords(
      change_log_search_criteria)[0]

  # Display the contents of each change log record.
  if results['records']:
    for change_log in results['records']:
      print ('Action \'%s\', Context \'%s\', Change Date \'%s\','
             ' New Value \'%s\', Old Value \'%s\', Profile Name \'%s\''
             ' was found.'
             % (change_log['action'],
                change_log['context'], change_log['changeDate'],
                change_log['newValue'], change_log['oldValue'],
                change_log['username']))
  else:
    print 'No change log entries found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, ADVERTISER_ID)
