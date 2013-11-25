#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Migrates legacy sitelinks to upgraded sitelinks for a list of campaigns.

The campaigns must be upgraded to enhanced campaigns before you
can run this example. To upgrade a campaign to enhanced, run
campaign_management/set_campaign_enhanced.py. To get all campaigns, run
basic_operations/get_campaigns.py.

Tags: CampaignAdExtensionService.get, CampaignAdExtensionService.mutate
Tags: FeedService.mutate, FeedItemService.mutate, FeedMappingService.mutate
Tags: CampaignFeedService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient

# See the Placeholder reference page for a list of all the placeholder types and
# fields.
# https://developers.google.com/adwords/api/docs/appendix/placeholders
PLACEHOLDER_SITELINKS = '1'
PLACEHOLDER_FIELD_SITELINK_LINK_TEXT = '1'
PLACEHOLDER_FIELD_SITELINK_LINK_URL = '2'


CAMPAIGN_IDS = ['INSERT_CAMPAIGN_ID_HERE', 'INSERT_CAMPAIGN_ID_HERE']


def main(client, campaign_ids):
  # Initialize appropriate service.
  campaign_ad_extension_service = client.GetCampaignAdExtensionService(
      version='v201306')
  feed_service = client.GetFeedService(version='v201306')
  feed_item_service = client.GetFeedItemService(version='v201306')
  feed_mapping_service = client.GetFeedMappingService(version='v201306')
  campaign_feed_service = client.GetCampaignFeedService(version='v201306')

  # Try to retrieve an existing feed that has been mapped for use with
  # sitelinks. If multiple such feeds exist, the first matching feed is
  # retrieved. You could modify this code example to retrieve all the feeds
  # and pick the appropriate feed based on user input.
  site_links_feed = GetExistingFeed(feed_mapping_service)

  if site_links_feed is None:
    # Create a feed for storing sitelinks.
    site_links_feed = CreateSiteLinksFeed(feed_service)

    # Map the feed for using with sitelinks.
    CreateSiteLinksFeedMapping(feed_mapping_service, site_links_feed)

  for campaign_id in campaign_ids:
    # Get legacy sitelinks for the campaign.
    extension = GetLegacySitelinksForCampaign(campaign_ad_extension_service,
                                              campaign_id)
    if extension is not None:
      # Get the sitelinks.
      legacy_site_links = extension['adExtension']['sitelinks']

      # Add the sitelinks to the feed.
      site_link_feed_item_ids = CreateSiteLinkFeedItems(
          feed_item_service, site_links_feed, legacy_site_links)

      # Associate feeditems to the campaign.
      AssociateSitelinkFeedItemsWithCampaign(
          campaign_feed_service, site_links_feed, site_link_feed_item_ids,
          campaign_id)

      # Once the upgraded sitelinks are added to a campaign, the legacy
      # sitelinks will stop serving. You can delete the legacy sitelinks
      # once you have verified that the migration went fine. In case the
      # migration didn't succeed, you can roll back the migration by deleting
      # the CampaignFeed you created in the previous step.
      DeleteLegacySitelinks(campaign_ad_extension_service, extension)


def GetExistingFeed(feed_mapping_service):
  """Retrieve an existing feed that is mapped to hold sitelinks.

  The first active sitelinks feed is retrieved by this method.

  Args:
    feed_mapping_service: The FeedMappingService instance.

  Returns:
    A dictionary represent a sitelinks feed if a feed was found, None otherwise.
  """
  selector = {
      'fields': ['FeedId', 'FeedMappingId', 'PlaceholderType', 'Status',
                 'AttributeFieldMappings'],
      'predicates': [
          {'field': 'PlaceholderType', 'operator': 'EQUALS',
           'values': [PLACEHOLDER_SITELINKS]},
          {'field': 'Status', 'operator': 'EQUALS', 'values': ['ACTIVE']}
      ],
  }

  page = feed_mapping_service.get(selector)[0]
  if page.get('entries'):
    for feed_mapping in page['entries']:
      feed_id = feed_mapping['feedId']
      text_attribute_id = None
      url_attribute_id = None
      for attribute_mapping in feed_mapping['attributeFieldMappings']:
        if attribute_mapping['fieldId'] == PLACEHOLDER_FIELD_SITELINK_LINK_TEXT:
          text_attribute_id = attribute_mapping['feedAttributeId']
        elif (attribute_mapping['fieldId'] ==
              PLACEHOLDER_FIELD_SITELINK_LINK_URL):
          url_attribute_id = attribute_mapping['feedAttributeId']

      if text_attribute_id is not None and url_attribute_id is not None:
        return {
            'siteLinksFeedId': feed_id,
            'textFeedAtrributeId': text_attribute_id,
            'urlFeedAttributeId': url_attribute_id
        }
  return None


def CreateSiteLinksFeed(feed_service):
  """Create a feed for holding upgraded sitelinks.

  Args:
    feed_service: The FeedService instance.

  Returns:
    A dictionary represent a sitelinks feed holding the sitelinks.
  """
  # Create attributes.
  text_attribute = {
      'type': 'STRING',
      'name': 'Link Text',
  }
  url_attribute = {
      'type': 'URL',
      'name': 'Link URL',
  }

  # Create the feed.
  site_links_feed = {
      'name': 'Feed For Sitelinks',
      'attributes': [text_attribute, url_attribute],
      'origin': 'USER'
  }

  # Create operation.
  operation = {
      'operand': site_links_feed,
      'operator': 'ADD'
  }

  # Add the feed.
  saved_feed = feed_service.mutate([operation])[0]['value'][0]

  return {
      'siteLinksFeedId': saved_feed['id'],
      'textFeedAtrributeId': saved_feed['attributes'][0]['id'],
      'urlFeedAttributeId': saved_feed['attributes'][1]['id']
  }


def CreateSiteLinksFeedMapping(feed_mapping_service, site_links_feed):
  """Map the feed for use with Sitelinks.

  Args:
    feed_mapping_service: The FeedMappingService instance.
    site_links_feed: The feed for holding sitelinks.
  """
  # Map the FeedAttributeIds to the fieldId constants.
  link_text_field_mapping = {
      'feedAttributeId': site_links_feed['textFeedAtrributeId'],
      'fieldId': PLACEHOLDER_FIELD_SITELINK_LINK_TEXT,
  }
  link_url_field_mapping = {
      'feedAttributeId': site_links_feed['urlFeedAttributeId'],
      'fieldId': PLACEHOLDER_FIELD_SITELINK_LINK_URL,
  }

  # Create the FieldMapping and operation.
  feed_mapping = {
      'placeholderType': PLACEHOLDER_SITELINKS,
      'feedId': site_links_feed['siteLinksFeedId'],
      'attributeFieldMappings': [link_text_field_mapping,
                                 link_url_field_mapping],
  }
  operation = {
      'operand': feed_mapping,
      'operator': 'ADD'
  }

  # Save the field mapping.
  feed_mapping_service.mutate([operation])


def GetLegacySitelinksForCampaign(campaign_extension_service, campaign_id):
  """Get legacy sitelinks for a campaign.

  Args:
    campaign_extension_service: The CampaignAdExtensionServiceInterface
                                instance.
    campaign_id: ID of the campaign for which legacy sitelinks are retrieved.

  Returns:
    The CampaignAdExtension that contains the legacy sitelinks, or None if there
    are no legacy sitelinks in this campaign.
  """
  # Filter the results for specified campaign id.
  campaign_predicate = {
      'operator': 'EQUALS',
      'field': 'CampaignId',
      'values': [campaign_id]
  }

  # Filter the results for active campaign ad extensions. You may add
  # additional filtering conditions here as required.
  status_predicate = {
      'operator': 'EQUALS',
      'field': 'Status',
      'values': ['ACTIVE']
  }

  # Filter for sitelinks ad extension type.
  type_predicate = {
      'operator': 'EQUALS',
      'field': 'AdExtensionType',
      'values': ['SITELINKS_EXTENSION']
  }

  # Create the selector.
  selector = {
      'fields': ['AdExtensionId', 'DisplayText', 'DestinationUrl'],
      'predicates': [campaign_predicate, status_predicate, type_predicate]
  }

  page = campaign_extension_service.get(selector)[0]
  if 'entries' in page and page['entries']:
    return page['entries'][0]
  else:
    return None


def CreateSiteLinkFeedItems(feed_item_service, site_links_feed, site_links):
  """Add legacy sitelinks to the sitelinks feed.

  Args:
    feed_item_service: The FeedItemServiceInterface instance.
    site_links_feed: The feed for adding sitelinks.
    site_links: The list of legacy sitelinks to be added to the feed.

  Returns:
    The list of feeditems that were added to the feed.
  """
  site_link_feed_item_ids = []

  # Create operations for adding each legacy sitelink to the sitelinks feed.
  feed_item_operations = []

  for site_link in site_links:
    feed_item_operations.append(NewSiteLinkFeedItemAddOperation(
        site_links_feed, site_link['displayText'],
        site_link['destinationUrl']))

  result = feed_item_service.mutate(feed_item_operations)[0]

  # Retrieve the feed item ids.
  for item in result['value']:
    site_link_feed_item_ids.append(item['feedItemId'])

  return site_link_feed_item_ids


def NewSiteLinkFeedItemAddOperation(site_links_feed, text, url):
  """Creates a new operation for adding a feed item.

  Args:
    site_links_feed: The sitelinks feed.
    text: The sitelink text.
    url: The sitelink url.

  Returns:
    A FeedItemOperation for adding the feed item.
  """
  # Create the FeedItemAttributeValues for our text values.
  link_text_attribute_value = {
      'feedAttributeId': site_links_feed['textFeedAtrributeId'],
      'stringValue': text,
  }
  link_url_attribute_value = {
      'feedAttributeId': site_links_feed['urlFeedAttributeId'],
      'stringValue': url,
  }

  # Create the feed item and operation.
  item = {
      'feedId': site_links_feed['siteLinksFeedId'],
      'attributeValues': [link_text_attribute_value, link_url_attribute_value]
  }
  operation = {
      'operand': item,
      'operator': 'ADD'
  }
  return operation


def DeleteLegacySitelinks(campaign_extension_service, extension_to_delete):
  """Delete legacy sitelinks from a campaign.

  Args:
    campaign_extension_service: The CampaignAdExtensionServiceInterface
                                instance.
    extension_to_delete: The CampaignAdExtension that holds legacy sitelinks.
  """
  operation = {
      'operator': 'REMOVE',
      'operand': extension_to_delete
  }
  campaign_extension_service.mutate([operation])


def AssociateSitelinkFeedItemsWithCampaign(
    campaign_feed_service, site_links_feed, site_link_feed_item_ids,
    campaign_id):
  """Associates sitelink feed items with a campaign.

  Args:
    campaign_feed_service: The CampaignFeedServiceInterface instance.
    site_links_feed: The feed for holding the sitelinks.
    site_link_feed_item_ids: The list of feed item ids to be associated with a
                             campaign as sitelinks.
    campaign_id: The campaign id to which upgraded sitelinks are added.
  """
  # Create a custom matching function that matches the given feed items to
  # the campaign.
  request_context_operand = {
      'xsi_type': 'RequestContextOperand',
      'contextType': 'FEED_ITEM_ID'
  }

  function = {
      'lhsOperand': [request_context_operand],
      'operator': 'IN'
  }

  operands = []
  for feed_item_id in site_link_feed_item_ids:
    constant_operand = {
        'xsi_type': 'ConstantOperand',
        'longValue': feed_item_id,
        'type': 'LONG'
    }
    operands.append(constant_operand)

  function['rhsOperand'] = operands

  # Create upgraded sitelinks for the campaign. Use the sitelinks feed we
  # created, and restrict feed items by matching function.
  campaign_feed = {
      'feedId': site_links_feed['siteLinksFeedId'],
      'campaignId': campaign_id,
      'matchingFunction': function,
      'placeholderTypes': [PLACEHOLDER_SITELINKS]
  }

  operation = {
      'operand': campaign_feed,
      'operator': 'ADD'
  }
  campaign_feed_service.mutate([operation])


if __name__ == '__main__':
  # Initialize client object.
  client_ = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client_, CAMPAIGN_IDS)
