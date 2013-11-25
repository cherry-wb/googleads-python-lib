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

"""This example adds several text ads to a given ad group. To get ad_group_id,
run get_ad_groups.py.

Tags: AdGroupAdService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient
from adspygoogle.common import Utils


ad_group_id = 'INSERT_AD_GROUP_ID_HERE'


def main(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_ad_service = client.GetAdGroupAdService(version='v201306')

  # Construct operations and add ads.
  operations = [
      {
          'operator': 'ADD',
          'operand': {
              'type': 'AdGroupAd',
              'adGroupId': ad_group_id,
              'ad': {
                  'type': 'ThirdPartyRedirectAd',
                  'name': 'Example third party ad #%s' % Utils.GetUniqueName(),
                  'url': 'http://www.example.com',
                  'dimensions': {
                      'width': '300',
                      'height': '250'
                  },
                  # This field normally contains the javascript ad tag.
                  'snippet': ('<img src="http://www.google.com/intl/en/adwords/'
                              'select/images/samples/inline.jpg"/>'),
                  'certifiedVendorFormatId': '232',
                  'isCookieTargeted': 'false',
                  'isUserInterestTargeted': 'false',
                  'isTagged': 'false',
                  'richMediaAdType': 'STANDARD',
                  'expandingDirections': ['EXPANDING_UP', 'EXPANDING_DOWN'],
                  'adAttributes': ['ROLL_OVER_TO_EXPAND']
              }
          }
      },
      {
          'operator': 'ADD',
          'operand': {
              'type': 'AdGroupAd',
              'adGroupId': ad_group_id,
              'ad': {
                  'type': 'ThirdPartyRedirectAd',
                  'name': 'Example third party ad #%s' % Utils.GetUniqueName(),
                  'url': 'http://www.example.com',
                  'adDuration': '15000',
                  'sourceUrl': ('http://ad.doubleclick.net/pfadx/N270.126913.'
                                '6102203221521/B3876671.21;dcadv=2215309;'
                                'sz=0x0;ord=%5btimestamp%5d;dcmt=text/xml'),
                  'certifiedVendorFormatId': '303',
                  'richMediaAdType': 'IN_STREAM_VIDEO'
              }
          }
      }
  ]
  ads = ad_group_ad_service.Mutate(operations)[0]

  # Display results.
  for ad in ads['value']:
    print ('Ad with ID \'%s\' and of type \'%s\' was added.'
           % (ad['ad']['id'], ad['ad']['Ad_Type']))

  print
  print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, ad_group_id)
