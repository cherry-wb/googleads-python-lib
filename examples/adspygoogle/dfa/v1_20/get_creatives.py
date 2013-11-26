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

"""This example retrieves available creatives for a given advertiser and
displays the name and ID. To create an advertiser, run CreateAdvertiser.java.
Results are limited to the first 10.

Tags: creative.getCreatives
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
  creative_service = client.GetCreativeService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Set up creative search criteria structure.
  page_number = 1
  creative_search_criteria = {
      'advertiserId': advertiser_id,
      'pageSize': '100',
      'pageNumber': str(page_number)
  }

  while True:
    # Get creatives for the selected criteria.
    results = creative_service.GetCreatives(creative_search_criteria)[0]

    # Display creative name and its ID.
    if results['records']:
      for creative in results['records']:
        print ('Creative with name \'%s\' and ID \'%s\' was found.'
               % (creative['name'], creative['id']))
    page_number += 1
    creative_search_criteria['pageNumber'] = str(page_number)
    if page_number > int(results['totalNumberOfPages']):
      break

  print 'Number of results found: %s' % results['totalNumberOfRecords']


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, ADVERTISER_ID)
