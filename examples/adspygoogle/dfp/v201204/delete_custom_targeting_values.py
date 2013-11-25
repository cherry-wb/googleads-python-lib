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

"""This example deletes custom targeting values for a given custom targeting
key. To determine which custom targeting keys and values exist, run
get_all_custom_targeting_keys_and_values.py."""

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
custom_targeting_service = client.GetService(
    'CustomTargetingService', version='v201204')

key_id = 'INSERT_CUSTOM_TARGETING_KEY_ID_HERE'
filter_values = [{
    'key': 'keyId',
    'value': {
        'xsi_type': 'NumberValue',
        'value': key_id
    }
}]
filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId',
                    'values': filter_values}

# Get custom targeting values.
response = custom_targeting_service.GetCustomTargetingValuesByStatement(
    filter_statement)[0]
values = []
if 'results' in response:
  values = response['results']
print 'Number of custom targeting values to be deleted: %s' % len(values)

if values:
  value_ids = [value['id'] for value in values]
  action = {'type': 'DeleteCustomTargetingValues'}
  filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId '
                      'AND id IN (%s)' % ', '.join(value_ids),
                      'values': filter_values}

  # Delete custom targeting keys.
  result = custom_targeting_service.PerformCustomTargetingValueAction(
      action, filter_statement)[0]

  # Display results.
  if result and result['numChanges'] > 0:
    print 'Number of custom targeting values deleted: %s' % result['numChanges']
  else:
    print 'No custom targeting values were deleted.'
