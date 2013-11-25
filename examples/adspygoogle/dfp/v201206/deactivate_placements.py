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

"""This code example deactivates all active placements. To determine which
placements exist, run get_all_placements.py."""

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
placement_service = client.GetService('PlacementService', version='v201206')

# Create query.
values = [{
    'key': 'status',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ACTIVE'
    }
}]
query = 'WHERE status = :status'

# Get placements by statement.
placements = DfpUtils.GetAllEntitiesByStatementWithService(
    placement_service, query=query, bind_vars=values)
for placement in placements:
  print ('Placement with id \'%s\', name \'%s\', and status \'%s\' will be '
         'deactivated.' % (placement['id'], placement['name'],
                           placement['status']))
print 'Number of placements to be deactivated: %s' % len(placements)

# Perform action.
result = placement_service.PerformPlacementAction(
    {'type': 'DeactivatePlacements'}, {'query': query, 'values': values})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of placements deactivated: %s' % result['numChanges']
else:
  print 'No placements were deactivated.'
