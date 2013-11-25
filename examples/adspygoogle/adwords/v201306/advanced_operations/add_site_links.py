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

"""This example adds a sitelinks feed and associates it with a campaign.

Tags: CampaignFeedService.mutate, FeedItemService.mutate
Tags: FeedMappingService.mutate, FeedService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient
from adspygoogle.common.Errors import Error

# See the Placeholder reference page for a list of all the placeholder types and
# fields.
# https://developers.google.com/adwords/api/docs/appendix/placeholders.html
PLACEHOLDER_SITELINKS = '1'
PLACEHOLDER_FIELD_SITELINK_LINK_TEXT = '1'
PLACEHOLDER_FIELD_SITELINK_LINK_URL = '2'

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'


def main(client, campaign_id):
  # Initialize appropriate service.
  feed_service = client.GetFeedService(version='v201306')
  feed_item_service = client.GetFeedItemService(version='v201306')
  feed_mapping_service = client.GetFeedMappingService(version='v201306')
  campaign_feed_service = client.GetCampaignFeedService(version='v201306')

  sitelinks_data = {}

  # Create site links feed first.
  site_links_feed = {
      'name': 'Feed For Site Links',
      'attributes': [
          {'type': 'STRING', 'name': 'Link Text'},
          {'type': 'URL', 'name': 'Link URL'}
      ]
  }

  response = feed_service.mutate([
      {'operator': 'ADD', 'operand': site_links_feed}
  ])[0]
  if 'value' in response:
    feed = response['value'][0]
    link_text_feed_attribute_id = feed['attributes'][0]['id']
    link_url_feed_attribute_id = feed['attributes'][1]['id']
    print ('Feed with name \'%s\' and ID \'%s\' was added with' %
           (feed['name'], feed['id']))
    print ('\tText attribute ID \'%s\' and URL attribute ID \'%s\'.' %
           (link_text_feed_attribute_id, link_url_feed_attribute_id))
    sitelinks_data['feedId'] = feed['id']
    sitelinks_data['linkTextFeedId'] = link_text_feed_attribute_id
    sitelinks_data['linkUrlFeedId'] = link_url_feed_attribute_id
  else:
    raise Error('No feeds were added.')

  # Create site links feed items.
  items_data = [
      {'text': 'Home', 'url': 'http://www.example.com'},
      {'text': 'Stores', 'url': 'http://www.example.com/stores'},
      {'text': 'On Sale', 'url': 'http://www.example.com/sale'},
      {'text': 'Support', 'url': 'http://www.example.com/support'},
      {'text': 'Products', 'url': 'http://www.example.com/products'},
      {'text': 'About', 'url': 'http://www.example.com/about'}
  ]

  feed_items = []
  for item in items_data:
    feed_items.append({
        'feedId': sitelinks_data['feedId'],
        'attributeValues': [
            {
                'feedAttributeId': sitelinks_data['linkTextFeedId'],
                'stringValue': item['text']
            },
            {
                'feedAttributeId': sitelinks_data['linkUrlFeedId'],
                'stringValue': item['url']
            }
        ]
    })

  feed_items_operations = [{'operator': 'ADD', 'operand': item} for item
                           in feed_items]

  response = feed_item_service.mutate(feed_items_operations)[0]
  if 'value' in response:
    sitelinks_data['feedItemIds'] = []
    for feed_item in response['value']:
      print 'Feed item with ID %s was added.' % feed_item['feedItemId']
      sitelinks_data['feedItemIds'].append(feed_item['feedItemId'])
  else:
    raise Error('No feed items were added.')

  # Create site links feed mapping.

  feed_mapping = {
      'placeholderType': PLACEHOLDER_SITELINKS,
      'feedId': sitelinks_data['feedId'],
      'attributeFieldMappings': [
          {
              'feedAttributeId': sitelinks_data['linkTextFeedId'],
              'fieldId': PLACEHOLDER_FIELD_SITELINK_LINK_TEXT
          },
          {
              'feedAttributeId': sitelinks_data['linkUrlFeedId'],
              'fieldId': PLACEHOLDER_FIELD_SITELINK_LINK_URL
          }
      ]
  }

  response = feed_mapping_service.mutate([
      {'operator': 'ADD', 'operand': feed_mapping}
  ])[0]
  if 'value' in response:
    feed_mapping = response['value'][0]
    print ('Feed mapping with ID %s and placeholder type %s was saved for feed'
           ' with ID %s.' %
           (feed_mapping['feedMappingId'], feed_mapping['placeholderType'],
            feed_mapping['feedId']))
  else:
    raise Error('No feed mappings were added.')

  # Create site links campaign feed.
  operands = []
  for feed_item_id in sitelinks_data['feedItemIds']:
    operands.append({
        'xsi_type': 'ConstantOperand',
        'type': 'LONG',
        'longValue': feed_item_id
    })

  feed_item_function = {
      'operator': 'IN',
      'lhsOperand': [
          {'xsi_type': 'RequestContextOperand', 'contextType': 'FEED_ITEM_ID'}
      ],
      'rhsOperand': operands
  }

  # Optional: to target to a platform, define a function and 'AND' it with the
  #           feed item ID link:
  platform_function = {
      'operator': 'EQUALS',
      'lhsOperand': [
          {
              'xsi_type': 'RequestContextOperand',
              'contextType': 'DEVICE_PLATFORM'
          }
      ],
      'rhsOperand': [
          {
              'xsi_type': 'ConstantOperand',
              'type': 'STRING',
              'stringValue': 'Mobile'
          }
      ]
  }
  combined_function = {
      'operator': 'AND',
      'lhsOperand': [
          {'xsi_type': 'FunctionOperand', 'value': feed_item_function},
          {'xsi_type': 'FunctionOperand', 'value': platform_function}
      ]
  }

  campaign_feed = {
      'feedId': sitelinks_data['feedId'],
      'campaignId': campaign_id,
      'matchingFunction': combined_function,
      # Specifying placeholder types on the CampaignFeed allows the same feed
      # to be used for different placeholders in different Campaigns.
      'placeholderTypes': [PLACEHOLDER_SITELINKS]
  }

  response = campaign_feed_service.mutate([
      {'operator': 'ADD', 'operand': campaign_feed}
  ])[0]
  if 'value' in response:
    campaign_feed = response['value'][0]
    print ('Campaign with ID %s was associated with feed with ID %s.' %
           (campaign_feed['campaignId'], campaign_feed['feedId']))
  else:
    raise Error('No campaign feeds were added.')


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, campaign_id)
