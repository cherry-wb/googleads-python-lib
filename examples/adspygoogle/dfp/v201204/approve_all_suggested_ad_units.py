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

"""This code example approves all suggested ad units with 50 or
more requests. This feature is only available to DFP premium solution
networks."""

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
suggested_ad_unit_service = client.GetService(
    'SuggestedAdUnitService', version='v201204')

query = 'WHERE numRequests >= :numRequests'
values = [{
    'key': 'numRequests',
    'value': {
        'xsi_type': 'NumberValue',
        'value': '50'
    }
}]

suggested_ad_units = DfpUtils.GetAllEntitiesByStatementWithService(
    suggested_ad_unit_service, query=query, bind_vars=values)

# Print suggested ad units that will be approved.
for suggested_ad_unit in suggested_ad_units:
  print ('Suggested ad unit with id \'%s\', and number of requests \'%s\' will'
         ' be approved.' % (suggested_ad_unit['id'],
                            suggested_ad_unit['numRequests']))
print 'Number of suggested ad units to approve: %s' % len(suggested_ad_units)

# Approve suggested ad units.
result = suggested_ad_unit_service.performSuggestedAdUnitAction(
    {'type': 'ApproveSuggestedAdUnit'},
    {'query': query, 'values': values})[0]

if result and int(result['numChanges']) > 0:
  print 'Number of suggested ad units approved: %s' % result['numChanges']
else:
  print 'No suggested ad units were approved.'


