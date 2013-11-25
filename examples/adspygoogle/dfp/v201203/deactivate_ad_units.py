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

"""This code example deactivates all active ad units. To determine which ad
units exist, run get_all_ad_units.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
inventory_service = client.GetService(
    'InventoryService', 'https://www.google.com', 'v201203')

# Create query.
values = [{
    'key': 'status',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ACTIVE'
    }
}]
query = 'WHERE status = :status'

# Get ad units by statement.
ad_units = DfpUtils.GetAllEntitiesByStatementWithService(
    inventory_service, query=query, bind_vars=values)
for ad_unit in ad_units:
  print ('Ad unit with id \'%s\', name \'%s\', and status \'%s\' will be '
         'deactivated.' % (ad_unit['id'], ad_unit['name'], ad_unit['status']))
print 'Number of ad units to be deactivated: %s' % len(ad_units)

# Perform action.
result = inventory_service.PerformAdUnitAction(
    {'type': 'DeactivateAdUnits'}, {'query': query, 'values': values})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of ad units deactivated: %s' % result['numChanges']
else:
  print 'No ad units were deactivated.'
