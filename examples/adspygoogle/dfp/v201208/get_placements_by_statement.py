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

"""This code example gets all active placements by using a statement. To create
a placement, run create_placements.py."""

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
placement_service = client.GetService('PlacementService', version='v201208')

# Create a statement to only select active placements.
values = [{
    'key': 'status',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ACTIVE'
    }
}]
filter_statement = {'query': 'WHERE status = :status LIMIT 500',
                    'values': values}

# Get placements by statement.
response = placement_service.GetPlacementsByStatement(filter_statement)[0]
placements = []
if 'results' in response:
  placements = response['results']

# Display results.
for placement in placements:
  print ('Placement with id \'%s\', name \'%s\', and status \'%s\' was found.'
         % (placement['id'], placement['name'], placement['status']))

print
print 'Number of results found: %s' % len(placements)
