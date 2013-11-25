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

"""This code example deactivates all active Labels. To determine which labels
exist, run get_all_labels.py.  This feature is only available to DFP premium
solution networks."""

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
label_service = client.GetService('LabelService', version='v201206')

# Create query.
values = [{
    'key': 'isActive',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'True'
    }
}]
query = 'WHERE isActive = :isActive'

# Get labels by statement.
labels = DfpUtils.GetAllEntitiesByStatementWithService(
    label_service, query=query, bind_vars=values)
for label in labels:
  print ('Label with id \'%s\' and name \'%s\' will be '
         'deactivated.' % (label['id'], label['name']))
print 'Number of Labels to be deactivated: %s' % len(labels)

# Perform action.
result = label_service.PerformLabelAction({'type': 'DeactivateLabels'},
                                          {'query': query, 'values': values})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of labels deactivated: %s' % result['numChanges']
else:
  print 'No labels were deactivated.'
