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

"""This code example creates a new video ad unit under the effective root ad
unit. This feature is only available to DFP premium solution networks. To
determine which ad units exist, run get_ad_unit_tree.py or
get_all_ad_units.py"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
inventory_service = client.GetService(
    'InventoryService', 'https://www.google.com', 'v201203')
network_service = client.GetService(
    'NetworkService', 'https://www.google.com', 'v201203')

# Set the parent ad unit's id for all ad units to be created under.
effective_root_ad_unit_id = \
    network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']

# Create ad unit object.
ad_unit = {
    'name': 'Video_Ad_Unit_%s' % Utils.GetUniqueName(),
    'parentId': effective_root_ad_unit_id,
    'description': 'Ad unit description.',
    'targetWindow': 'BLANK',
    'adUnitSizes': [
        {
            'size': {
                'width': '400',
                'height': '300'
            },
            'environmentType': 'VIDEO_PLAYER',
            'companions': [
                {
                    'size': {
                        'width': '300',
                        'height': '250'
                    },
                    'environmentType': 'BROWSER'
                },
                {
                    'size': {
                        'width': '728',
                        'height': '90'
                    },
                    'environmentType': 'BROWSER'
                }
            ]
        }
    ],
    'targetPlatform': 'WEB'
}

# Add ad unit.
ad_unit = inventory_service.CreateAdUnit(ad_unit)[0]

# Display results.
print ('Video ad unit with id \'%s\' was created under parent with id \'%s\'.'
       % (ad_unit['id'], effective_root_ad_unit_id))
