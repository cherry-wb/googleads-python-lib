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

"""This example displays advertiser name, ID and spotlight configuration ID for
the given search criteria. Results are limited to first 10 records.

Tags: advertiser.getAdvertisers
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  advertiser_service = client.GetAdvertiserService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Create advertiser search criteria structure.
  page_number = 1
  advertiser_search_criteria = {
      'pageSize': '100',
      'pageNumber': str(page_number)
  }

  while True:
    # Get advertiser record set.
    results = advertiser_service.GetAdvertisers(advertiser_search_criteria)[0]

    # Display advertiser names, IDs and spotlight configuration IDs.
    if results['records']:
      for advertiser in results['records']:
        print ('Advertiser with name \'%s\', ID \'%s\', and spotlight '
               'configuration id \'%s\' was found.'
               % (advertiser['name'], advertiser['id'], advertiser['spotId']))
    page_number += 1
    advertiser_search_criteria['pageNumber'] = str(page_number)
    if page_number > int(results['totalNumberOfPages']):
      break

  print 'Number of results found: %s' % results['totalNumberOfRecords']


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
