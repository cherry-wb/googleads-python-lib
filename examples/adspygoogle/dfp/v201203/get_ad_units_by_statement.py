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

"""This code example gets the root ad unit by using a statement. To create an ad
unit, run create_ad_unit.py."""

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
network_service = client.GetService(
    'NetworkService', 'https://www.google.com', 'v201203')

# Get the effective root ad unit ID of the network.
effective_root_ad_unit_id = \
    network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']

# Create a statement to select the children of the effective root ad unit.
values = [{
    'key': 'id',
    'value': {
        'xsi_type': 'TextValue',
        'value': effective_root_ad_unit_id
    }
}]
filter_statement = {'query': 'WHERE parentId = :id LIMIT 1',
                    'values': values}

# Get ad units by statement.
response = inventory_service.GetAdUnitsByStatement(filter_statement)[0]
ad_units = []
if 'results' in response:
  ad_units = response['results']

# Display results.
for ad_unit in ad_units:
  print ('Ad unit with id \'%s\', name \'%s\', and status \'%s\' was found.'
         % (ad_unit['id'], ad_unit['name'], ad_unit['status']))

print
print 'Number of results found: %s' % len(ad_units)
