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

"""This example adds campaigns. To get campaigns, run get_campaigns.py.

Tags: CampaignService.mutate
Tags: BudgetService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient
from adspygoogle.common import Utils
import datetime


def main(client):
  # Initialize appropriate service.
  campaign_service = client.GetCampaignService(version='v201302')
  budget_service = client.GetBudgetService(version='v201302')

  # Create a budget, which can be shared by multiple campaigns.
  budget = {
      'name': 'Interplanetary budget #%s' % Utils.GetUniqueName(),
      'amount': {
          'microAmount': '50000000'
      },
      'deliveryMethod': 'STANDARD',
      'period': 'DAILY'
  }

  budget_operations = [{
      'operator': 'ADD',
      'operand': budget
  }]

  # Add the budget.
  budget_id = budget_service.Mutate(budget_operations)[0]['value'][0][
      'budgetId']

  # Construct operations and add campaigns.
  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': 'Interplanetary Cruise #%s' % Utils.GetUniqueName(),
          'status': 'PAUSED',
          'biddingStrategy': {
              'xsi_type': 'ManualCPM'
          },
          'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'settings': [{
              'xsi_type': 'RealTimeBiddingSetting',
              'optIn': 'true'
          }, {
              'xsi_type': 'KeywordMatchSetting',
              'optIn': 'false'
          }],
          'networkSetting': {
              'targetContentNetwork': 'true',
          },
          # Optional fields
          'startDate': (datetime.datetime.now() +
                        datetime.timedelta(1)).strftime('%Y%m%d'),
          'adServingOptimizationStatus': 'ROTATE',
          'frequencyCap': {
              'impressions': '5',
              'timeUnit': 'DAY',
              'level': 'ADGROUP'
          }
      }
  }, {
      'operator': 'ADD',
      'operand': {
          'name': 'Interplanetary Cruise Banners #%s' % Utils.GetUniqueName(),
          'status': 'PAUSED',
          'biddingStrategy': {
              'xsi_type': 'ManualCPM'
          },
          'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'settings': [{
              'xsi_type': 'RealTimeBiddingSetting',
              'optIn': 'true'
          }, {
              'xsi_type': 'KeywordMatchSetting',
              'optIn': 'false'
          }],
          'networkSetting': {
              'targetContentNetwork': 'true',
          }
      }
  }]
  campaigns = campaign_service.Mutate(operations)[0]

  # Display results.
  for campaign in campaigns['value']:
    print ('Campaign with name \'%s\' and id \'%s\' was added.'
           % (campaign['name'], campaign['id']))

  print
  print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client)
