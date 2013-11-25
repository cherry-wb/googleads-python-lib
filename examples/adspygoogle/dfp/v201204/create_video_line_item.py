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

"""This code example creates a new line item to serve to video content. This
feature is only available to DFP premium solution networks. To determine which
line items exist, run get_all_line_items.py. To determine which orders exist,
run get_all_orders.py. To create a video ad unit, run create_video_ad_unit.py.
To create criteria for categories, run
create_custom_targeting_keys_and_values.py"""

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
line_item_service = client.GetService('LineItemService', version='v201204')

# Set order that all created line item will belong to and the video ad unit id
# to target.
order_id = 'INSERT_ORDER_ID_HERE'
targeted_video_ad_unit_id = 'INSERT_TARGETED_VIDEO_AD_UNIT_ID_HERE'

# Set the custom targeting key ID and value ID representing the metadata on the
# content to target. This would typically be a key representing a 'genre' and
# a value representing something like 'comedy'.
content_custom_targeting_key_id = 'INSERT_CONTENT_CUSTOM_TARGETING_KEY_ID_HERE'
content_custom_targeting_value_id = \
    'INSERT_CONTENT_CUSTOM_TARGETING_VALUE_ID_HERE'

# create custom criteria for the content metadata targeting.
custom_criteria = {
    'xsi_type': 'CustomCriteria',
    'keyId': content_custom_targeting_key_id,
    'valueIds': [content_custom_targeting_value_id],
    'operator': 'IS'
}

# Create the custom criteria set.
top_set = {
    'xsi_type': 'CustomCriteriaSet',
    'logicalOperator': 'OR',
    'children': [custom_criteria]
}

# Create line item object.
line_item = {
    'name': 'Line item #%s' % Utils.GetUniqueName(),
    'orderId': order_id,
    'targeting': {
        'customTargeting': top_set,
        'inventoryTargeting': {
            'targetedAdUnits': [{'adUnitId': targeted_video_ad_unit_id,
                                 'includeDescendants': 'True'}]
        },
        'videoPositionTargeting': {
            'targetedVideoPositions': ['PREROLL']
        }
    },
    'creativePlaceholders': [
        {
            'size': {
                'width': '400',
                'height': '300'
            },
            'companions': [
                {
                    'size': {
                        'width': '300',
                        'height': '250'
                    },
                },
                {
                    'size': {
                        'width': '728',
                        'height': '90'
                    },
                }
            ]
        }
    ],
    'environmentType': 'VIDEO_PLAYER',
    'companionDeliveryOption': 'OPTIONAL',
    'startDateTimeType': 'IMMEDIATELY',
    'lineItemType': 'SPONSORSHIP',
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
    'creativeRotationType': 'OPTIMIZED',
    'discountType': 'PERCENTAGE',
    'unitsBought': '100',
    'unitType': 'IMPRESSIONS',
    'allowOverbook': 'True'
}

# Add line item.
line_item = line_item_service.CreateLineItem(line_item)[0]

# Display results.
print ('Video line item with id \'%s\', belonging to order id \'%s\', and named'
       ' \'%s\' was created.' % (line_item['id'], line_item['orderId'],
                                 line_item['name']))
