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

"""This code example gets an ad unit by its id. To determine which ad units
exist, run get_ad_unit_tree.py or get_all_ad_units.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
inventory_service = client.GetService(
    'InventoryService', 'https://www.google.com', 'v201203')

# Set the id of the ad unit to get.
ad_unit_id = 'INSERT_AD_UNIT_ID_HERE'

# Get ad unit.
ad_unit = inventory_service.GetAdUnit(ad_unit_id)[0]

# Display results.
print ('Ad unit with id \'%s\', name \'%s\', and status \'%s\' was found.'
       % (ad_unit['id'], ad_unit['name'], ad_unit['status']))
