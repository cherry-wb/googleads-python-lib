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

"""This example sets a bid modifier for the mobile platform on given campaign.

NOTE: the campaign must be an enhanced type of campaign. To get campaigns, run
get_campaigns.py. To enhance a campaign, run set_campaign_enhanced.py.

Tags: CampaignCriterionService.mutate
"""

__author__ = 'api.dklimkin@gmail.com (Danial Klimkin)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


campaign_id = 'INSERT_CAMPAIGN_ID_HERE'
bid_modifier = '1.5'


def main(client, campaign_id, bid_modifier):
  # Initialize appropriate service.
  campaign_criterion_service = client.GetCampaignCriterionService(
      version='v201306')

  # Create mobile platform.The ID can be found in the documentation.
  # https://developers.google.com/adwords/api/docs/appendix/platforms
  mobile = {
      'xsi_type': 'Platform',
      'id': '30001'
  }

  # Create campaign criterion with modified bid.
  campaign_criterion = {
      'campaignId': campaign_id,
      'criterion': mobile,
      'bidModifier': bid_modifier
  }

  # Create operations.
  operations = [
      {
          'operator': 'SET',
          'operand': campaign_criterion
      }
  ]

  # Make the mutate request.
  result = campaign_criterion_service.mutate(operations)[0]

  # Display the resulting campaign criteria.
  for campaign_criterion in result['value']:
    print ('Campaign criterion with campaign id \'%s\' and criterion id \'%s\' '
           'was updated with bid modifier \'%s\'.'
           % (campaign_criterion['campaignId'],
              campaign_criterion['criterion']['id'],
              campaign_criterion['bidModifier']))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, campaign_id, bid_modifier)
