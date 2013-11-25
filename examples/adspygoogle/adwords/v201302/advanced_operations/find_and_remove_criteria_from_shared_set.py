#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License")
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

"""Finds a removes a shared set criterion from a campaign.

This example demonstrates how to find shared sets, shared set criteria, and
how to remove them.

Note: Shared sets is a Beta feature.

Tags: CampaignSharedSetService.mutate, CampaignSharedSetService.get
Tags: SharedCriterionService.get
Api: AdWordsOnly
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


CAMPAIGN_ID = 'INSERT_CAMPAIGN_HERE'
PAGE_SIZE = '500'


def main(client, campaign_id):
  # Initialize appropriate service.
  campaign_shared_set_service = client.GetCampaignSharedSetService(
      version='v201302')
  shared_criterion_service = client.GetSharedCriterionService(version='v201302')

  shared_set_ids = []
  criterion_ids = []

  # First, retrieve all shared sets associated with the campaign.

  # Create selector for shared sets to:
  # - filter by campaign ID,
  # - filter by shared set type.
  selector = {
      'fields': ['SharedSetId', 'CampaignId', 'SharedSetName', 'SharedSetType',
                 'Status'],
      'predicates': [
          {'field': 'CampaignId', 'operator': 'EQUALS',
           'values': [campaign_id]},
          {'field': 'SharedSetType', 'operator': 'IN', 'values':
           ['NEGATIVE_KEYWORDS', 'NEGATIVE_PLACEMENTS']}
      ],
      'paging': {
          'startIndex': '0',
          'numberResults': PAGE_SIZE
      }
  }

  # Set initial values.
  offset, page = '0', {}
  has_more_results = True

  while has_more_results:
    page = campaign_shared_set_service.get(selector)[0]
    for shared_set in page['entries']:
      print ('Campaign shared set ID %s and name \'%s\'' %
             (shared_set['sharedSetId'], shared_set['sharedSetName']))
      shared_set_ids.append(shared_set['sharedSetId'])

    # Increment values to request the next page.
    offset = str(int(offset) + int(PAGE_SIZE))
    selector['paging']['startIndex'] = offset
    has_more_results = page['totalNumEntries'] > offset

  # Next, Retrieve criterion IDs for all found shared sets.
  selector = {
      'fields': ['SharedSetId', 'Id', 'KeywordText', 'KeywordMatchType',
                 'PlacementUrl'],
      'predicates': [
          {'field': 'SharedSetId', 'operator': 'IN', 'values': shared_set_ids}
      ],
      'paging': {
          'startIndex': '0',
          'numberResults': PAGE_SIZE
      }
  }

  # Set initial values.
  offset, page = '0', {}

  while True:
    page = shared_criterion_service.get(selector)[0]
    for shared_criterion in page['entries']:
      if shared_criterion['criterion']['type'] == 'KEYWORD':
        print ('Shared negative keyword with ID %s and text \'%s\' was found.' %
               (shared_criterion['criterion']['id'],
                shared_criterion['criterion']['text']))
      elif shared_criterion['criterion']['type'] == 'PLACEMENT':
        print ('Shared negative placement with ID %s and url \'%s\' was found.'
               % (shared_criterion['criterion']['id'],
                  shared_criterion['criterion']['url']))
      else:
        print ('Shared criterion with ID %s was found.' %
               shared_criterion['criterion']['id'])
      criterion_ids.append({
          'sharedSetId': shared_criterion['sharedSetId'],
          'criterionId': shared_criterion['criterion']['id']
      })
    # Increment values to request the next page.
    offset = str(int(offset) + int(PAGE_SIZE))
    selector['paging']['startIndex'] = offset
    if not page['totalNumEntries'] > offset:
      break

  # Finally, remove the criteria.
  operations = []
  for criterion in criterion_ids:
    operation = {
        'operator': 'REMOVE',
        'operand': {
            'criterion': {'id': criterion['criterionId']},
            'sharedSetId': criterion['sharedSetId']
        }
    }
    operations.append(operation)

  response = shared_criterion_service.mutate(operations)[0]
  for criterion in response['value']:
    print ('Criterion ID %s was successfully removed from shared set ID %s.' %
           (criterion['criterion']['id'], criterion['sharedSetId']))


if __name__ == '__main__':
  # Initialize client object.
  CLIENT = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(CLIENT, CAMPAIGN_ID)
