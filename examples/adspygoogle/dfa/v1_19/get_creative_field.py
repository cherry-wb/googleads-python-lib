#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""This example retrieves available creative fields for a given string and
displays the name, ID, advertiser ID, and number of values. Results are
limited to the first 10.

Tags: creativefield.getCreativeFields
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
  creative_field_service = client.GetCreativeFieldService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Set up creative field search criteria structure.
  creative_field_search_criteria = {
      'advertiserIds': [advertiser_id],
      'pageSize': '10'
  }

  # Get creative fields for the selected criteria.
  results = creative_field_service.GetCreativeFields(
      creative_field_search_criteria)[0]

  # Display creative field names, IDs, advertiser IDs, and number of values.
  if results['records']:
    for creative_field in results['records']:
      print ('Creative field with name \'%s\', ID \'%s\', advertiser ID \'%s\','
             ' and containing \'%s\' values was found.'
             % (creative_field['name'], creative_field['id'],
                creative_field['advertiserId'],
                creative_field['totalNumberOfValues']))
  else:
    print 'No creative fields found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, ADVERTISER_ID)
