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

"""Test utility functions."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import base64
from datetime import date
import os
from adspygoogle.common import Utils


def CreateTestAdvertiser(client, server, version):
  """Create a test advertiser.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.

  Returns:
    The ID of the test advertiser.
  """
  company_service = client.GetService('CompanyService', server, version)

  # Create company object.
  company = {
      'name': 'Company #%s' % Utils.GetUniqueName(),
      'type': 'ADVERTISER'
  }

  # Add the company.
  companies = company_service.CreateCompanies([company])
  return companies[0]['id']


def GetEffectiveRootAdUnitId(client, server, version):
  """Get the effective root ad unit ID.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.

  Returns:
    The effective root ad unit ID.
  """
  network_service = client.GetService('NetworkService', server, version)
  return network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']


def CreateTestLineItemCustomField(client, server, version, data_type):
  """Create a test line item custom field.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    data_type: str the type of the custom field. Options are: STRING, NUMBER,
        TOGGLE, DROP_DOWN.

  Returns:
    The ID of the test drop-down custom field.
  """
  custom_field_service = client.GetService(
      'CustomFieldService', server, version)

  # Create custom field.
  custom_field = {
      'name': 'Test custom field #%s' % Utils.GetUniqueName(),
      'entityType': 'LINE_ITEM',
      'dataType': data_type,
      'visibility': 'FULL',
      'description': 'Test custom field.'
  }

  # Add the custom field.
  custom_fields = custom_field_service.CreateCustomFields([custom_field])
  return custom_fields[0]['id']


def CreateTestLineItemCustomFieldOption(client, server, version,
                                        drop_down_custom_field_id):
  """Create a test line item drop-down custom field option.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    drop_down_custom_field_id: str the ID of the drop-down custom field

  Returns:
    The ID of the test drop-down custom field.
  """
  custom_field_service = client.GetService(
      'CustomFieldService', server, version)

  # Create custom field option.
  custom_field_option = {
      'displayName': 'Approved #%s' % Utils.GetUniqueName(),
      'customFieldId': drop_down_custom_field_id
  }

  # Add custom field options.
  custom_field_options = custom_field_service.CreateCustomFieldOptions(
      [custom_field_option])
  return custom_field_options[0]['id']


def CreateTestLineItem(client, server, version, order_id, placement_ids):
  """Create a test line item.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    order_id: str the order the line item belongs to.
    placement_ids: list the ID's of the placement to target.

  Returns:
    The ID of the test line item.
  """
  line_item_service = client.GetService('LineItemService', server, version)

  # Create line item.
  line_item = {
      'name': 'Line item #%s' % Utils.GetUniqueName(),
      'orderId': order_id,
      'targeting': {
          'inventoryTargeting': {
              'targetedPlacementIds': placement_ids
          }
      },
      'creativePlaceholders': [
          {
              'size': {
                  'width': '300',
                  'height': '250'
              }
          },
          {
              'size': {
                  'width': '120',
                  'height': '600'
              }
          }
      ],
      'startDateTimeType': 'IMMEDIATELY',
      'lineItemType': 'STANDARD',
      'endDateTime': {
          'date': {
              'year': str(date.today().year + 1),
              'month': '9',
              'day': '30'
          },
          'hour': '0',
          'minute': '0',
          'second': '0'
      },
      'costType': 'CPM',
      'costPerUnit': {
          'currencyCode': 'USD',
          'microAmount': '2000000'
      },
      'creativeRotationType': 'EVEN',
      'discountType': 'PERCENTAGE',
      'unitsBought': '500000',
      'unitType': 'IMPRESSIONS',
      'allowOverbook': 'true'
  }

  # Add the line item.
  line_items = line_item_service.CreateLineItems([line_item])
  return line_items[0]['id']


def CreateTestOrder(client, server, version, advertiser_id, trafficker_id):
  """Create a test order.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    advertiser_id: str the company ID for the order's advertiser.
    trafficker_id: str the ID of the user trafficking this order.

  Returns:
    The ID of the test order.
  """
  order_service = client.GetService('OrderService', server, version)

  # Create order.
  order = {
      'name': 'Order #%s' % Utils.GetUniqueName(),
      'advertiserId': advertiser_id,
      'traffickerId': trafficker_id
  }

  # Add the order.
  orders = order_service.CreateOrders([order])
  return orders[0]['id']


def CreateTestPlacement(client, server, version, ad_units):
  """Create a test placement.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    ad_units: list ad units to target.

  Returns:
    The ID of the placement.
  """
  placement_service = client.GetService('PlacementService', server, version)

  # Create placement.
  placement = {
      'name': 'Test Placement #%s' % Utils.GetUniqueName(),
      'description': 'A test placement',
      'targetedAdUnitIds': ad_units
  }

  # Add the placement.
  placements = placement_service.CreatePlacements([placement])
  return placements[0]['id']


def CreateTestAdUnit(client, server, version):
  """Create a test ad unit.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.

  Returns:
    The ID of the ad unit.
  """
  inventory_service = client.GetService('InventoryService', server, version)
  network_service = client.GetService('NetworkService', server, version)

  # Set the parent ad unit's id for all ad units to be created under.
  parent_id = network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']

  # Create the ad unit.
  ad_unit = {
      'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
      'parentId': parent_id,
      'description': 'Test ad unit description.',
      'targetWindow': 'BLANK',
      'adUnitSizes': [
          {
              'size': {
                  'width': '300',
                  'height': '250'
              },
              'environmentType': 'BROWSER'
          }
      ]
  }

  # Add the ad unit.
  ad_units = inventory_service.CreateAdUnits([ad_unit])
  return ad_units[0]['id']


def GetTrafficker(client, server, version):
  """Gets a user that can serve as an order's trafficker.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.

  Returns:
    The ID of the trafficker.
  """
  user_service = client.GetService(
      'UserService', server, version)

  values = [{
      'key': 'trafficker',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'TRAFFICKER'
      }
  }, {
      'key': 'administrator',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'ADMINISTRATOR'
      }
  }]

  # The trafficker or administrator role can both be an order's trafficker.
  filter_statement = {
      'query': 'WHERE rolename = :trafficker or rolename = :administrator ',
      'values': values
  }

  # Get users by statement.
  response = user_service.GetUsersByStatement(filter_statement)[0]
  return response['results'][0]['id']


def CreateTestCreative(client, server, version, advertiser_id):
  """Create a test creative.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    advertiser_id: str the company ID for the creative's advertiser.

  Returns:
    The ID of the creative.
  """
  creative_service = client.GetService('CreativeService', server, version)

  # Create creative object.
  image_data = Utils.ReadFile(os.path.join(__file__[:__file__.rfind('/')], '..',
                                           'data', 'medium_rectangle.jpg'))
  image_data = base64.encodestring(image_data)

  creative = {
      'type': 'ImageCreative',
      'name': 'Image Creative #%s' % Utils.GetUniqueName(),
      'advertiserId': advertiser_id,
      'destinationUrl': 'http://google.com',
      'imageName': 'image.jpg',
      'imageByteArray': image_data,
      'size': {'width': '300', 'height': '250'}
  }

  # Add creatives.
  creatives = creative_service.CreateCreatives([creative])
  return creatives[0]['id']


def CreateTestCreativeSet(client, server, version, master_creative_id,
                          companion_creative_id):
  """Create a test creative.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    master_creative_id: str creative ID for the master.
    companion_creative_id: str creative ID for a companion.

  Returns:
    The ID of the creative.
  """
  creative_set_service = client.GetService('CreativeSetService', server,
                                           version)

  # Create creative set objects.
  creative_sets = {'name': 'Creative set #%s' % Utils.GetUniqueName(),
                   'masterCreativeId': master_creative_id,
                   'companionCreativeIds': [companion_creative_id]}

  # Add creative sets.
  creative_sets = creative_set_service.CreateCreativeSet(creative_sets)
  return creative_sets[0]['id']


def CreateTestLabel(client, server, version):
  """Create a test label of type creative wrapper.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.

  Returns:
    The ID of the test label.
  """
  label_service = client.GetService('LabelService', server, version)

  # Create label object.
  label = {
      'name': 'Test creative wrapper label #%s' % Utils.GetUniqueName(),
      'isActive': 'True',
      'types': ['CREATIVE_WRAPPER']
  }

  # Add the label.
  labels = label_service.CreateLabels([label])
  return labels[0]['id']


def CreateTestCreativeWrapper(client, server, version, label_id):
  """Create a test creative wrapper.

  Args:
    client: DfpClient used for service creation.
    server: str the API server.
    version: str the API version.
    label_id: str the id of the label the creative wrapper applies to.

  Returns:
    The ID of the test creative wrapper.
  """
  creative_wrapper_service = client.GetService('CreativeWrapperService', server,
                                               version)

  # Create creative wrapper object.
  creative_wrapper = {
      'labelId': label_id,
      'ordering': 'INNER',
      'header': {'htmlSnippet': '<b>My creative wrapper header</b>'}
  }

  # Add creative wrapper.
  creative_wrappers = creative_wrapper_service.CreateCreativeWrappers(
      [creative_wrapper])
  return creative_wrappers[0]['id']
