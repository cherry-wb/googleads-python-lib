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

"""Retrieves the ad group level bid modifiers for a campaign.

Tags: AdGroupBidModifierService.get
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


PAGE_SIZE = 500


def main(client):
  # Initialize appropriate service.
  ad_group_bid_modifier_service = client.GetAdGroupBidModifierService(
      version='v201302')

  # Get all ad group bid modifiers for the campaign.
  selector = {
      'fields': ['CampaignId', 'AdGroupId', 'BidModifier', 'Id'],
      'paging': {
          'startIndex': '0',
          'numberResults': str(PAGE_SIZE)
      }
  }

  # Set initial values.
  offset, page = 0, {}
  more_results = True

  while more_results:
    page = ad_group_bid_modifier_service.get(selector)[0]
    if page['entries']:
      for modifier in page['entries']:
        value = modifier.get('bidModifier') or 'unset'
        print ('Campaign ID %s, AdGroup ID %s, Criterion ID %s has ad group '
               'level modifier: %s' %
               (modifier['campaignId'], modifier['adGroupId'],
                modifier['criterion']['id'], value))

      # Increment values to request the next page.
      offset += PAGE_SIZE
      selector['paging']['startIndex'] = str(offset)
    else:
      print 'No ad group bid modifiers returned.'
    more_results = int(page['totalNumEntries']) > offset


if __name__ == '__main__':
  # Initialize client object.
  client_ = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client_)
