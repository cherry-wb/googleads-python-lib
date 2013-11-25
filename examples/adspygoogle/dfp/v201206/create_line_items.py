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

"""This code example creates new line items. To determine which line items
exist, run get_all_line_items.py. To determine which orders exist, run
get_all_orders.py. To determine which placements exist, run
get_all_placements.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
from datetime import date
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
line_item_service = client.GetService('LineItemService', version='v201206')

# Set order that all created line items will belong to and the placement id to
# target.
order_id = 'INSERT_ORDER_ID_HERE'
targeted_placement_ids = ['INSERT_PLACEMENT_ID_HERE']

# Create line item objects.
line_items = []
for i in xrange(5):
  line_item = {
      'name': 'Line item #%s' % Utils.GetUniqueName(),
      'orderId': order_id,
      'targeting': {
          'inventoryTargeting': {
              'targetedPlacementIds': targeted_placement_ids
          },
          'geoTargeting': {
              'targetedLocations': [
                  {
                      'id': '2840',
                      'xsi_type': 'CountryLocation',
                      'countryCode': 'US'
                  },
                  {
                      'id': '20123',
                      'xsi_type': 'RegionLocation',
                      'regionCode': 'CA-QC'
                  },
                  {
                      'id': '9000093',
                      'xsi_type': 'PostalCodeLocation',
                      'postalCode': 'B3P',
                      'countryCode': 'CA'
                  }
              ],
              'excludedLocations': [
                  {
                      'id': '1016367',
                      'xsi_type': 'CityLocation',
                      'cityName': 'Chicago',
                      'countryCode': 'US'
                  },
                  {
                      'id': '200501',
                      'xsi_type': 'MetroLocation',
                      'metroCode': '501'
                  }
              ]
          },
          'dayPartTargeting': {
              'dayParts': [
                  {
                      'dayOfWeek': 'SATURDAY',
                      'startTime': {
                          'hour': '0',
                          'minute': 'ZERO'
                      },
                      'endTime': {
                          'hour': '24',
                          'minute': 'ZERO'
                      }
                  },
                  {
                      'dayOfWeek': 'SUNDAY',
                      'startTime': {
                          'hour': '0',
                          'minute': 'ZERO'
                      },
                      'endTime': {
                          'hour': '24',
                          'minute': 'ZERO'
                      }
                  }
              ],
              'timeZone': 'BROWSER'
          },
          'userDomainTargeting': {
              'domains': ['usa.gov'],
              'targeted': 'false'
          },
          'technologyTargeting': {
              'browserTargeting': {
                  'browsers': [{'id': '500072'}],
                  'isTargeted': 'true'
              }
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
  line_items.append(line_item)

# Add line items.
line_items = line_item_service.CreateLineItems(line_items)

# Display results.
for line_item in line_items:
  print ('Line item with id \'%s\', belonging to order id \'%s\', and named '
         '\'%s\' was created.' % (line_item['id'], line_item['orderId'],
                                  line_item['name']))
