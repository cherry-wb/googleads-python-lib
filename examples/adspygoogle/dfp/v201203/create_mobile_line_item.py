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

"""This code example creates a new mobile line item. Mobile features needs to be
enabled in your account to use mobile targeting. To determine which line
items exist, run get_all_line_items.py. To determine which orders exist, run
get_all_orders.py. To determine which placements exist, run
get_all_placements.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

from datetime import date
import os
# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
line_item_service = client.GetService(
    'LineItemService', 'https://www.google.com', 'v201203')

# Set order that the created line item will belong to and add the id of a
# placement containing ad units with a mobile target platform.
order_id = 'INSERT_ORDER_ID_HERE'
targeted_placement_ids = ['INSERT_MOBILE_PLACEMENT_ID_HERE']

# Create the line item.
# Target the line items in the following manner:
# Target the Google device manufacturer (40100) but exclude the Nexus One
# device (604046).
# Target the iPhone 4 device submodel (640003).
line_item = {
    'name': 'Mobile line item #%s' % Utils.GetUniqueName(),
    'orderId': order_id,
    'targetPlatform': 'MOBILE',
    'targeting': {
        'inventoryTargeting': {
            'targetedPlacementIds': targeted_placement_ids
        },
        'technologyTargeting': {
            'deviceManufacturerTargeting': {
                'deviceManufacturers': [{'id': '40100'}],
                'isTargeted': 'true'
            },
            'mobileDeviceTargeting': {
                'targetedMobileDevices': [],
                'excludedMobileDevices': [{'id': '604046'}]
            },
            'mobileDeviceSubmodelTargeting': {
                'targetedMobileDeviceSubmodels': [{'id': '640003'}],
                'excludedMobileDeviceSubmodels': []
            }
        }
    },
    'creativePlaceholders': [
        {
            'size': {
                'width': '300',
                'height': '250'
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
    'unitType': 'IMPRESSIONS'
}

line_item = line_item_service.CreateLineItem(line_item)[0]

# Display results.
print ('Line item with id \'%s\', belonging to order id \'%s\', and named '
       '\'%s\' was created.' % (line_item['id'], line_item['orderId'],
                                line_item['name']))
