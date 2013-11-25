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

"""This example gets custom targeting values for the given predefined custom
targeting key. The statement retrieves up to the maximum page size limit of
500. To create custom targeting values, run
create_custom_targeting_keys_and_values.py. To determine which custom
targeting keys exist, run get_all_custom_targeting_keys_and_values.py."""

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
    'CustomTargetingService', version='v201208')

key_id = 'INSERT_CUSTOM_TARGETING_KEY_ID_HERE'
values = [{
    'key': 'keyId',
    'value': {
        'xsi_type': 'NumberValue',
        'value': key_id
    }
}]
filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId LIMIT 500',
                    'values': values}

# Get custom targeting values by statement.
response = custom_targeting_service.GetCustomTargetingValuesByStatement(
    filter_statement)[0]
values = []
if 'results' in response:
  values = response['results']

# Display results.
if values:
  for value in values:
    print ('Custom targeting value with id \'%s\', name \'%s\', and display '
           'name \'%s\' was found.'
           % (value['id'], value['name'], value['displayName']))
else:
  print 'No values were found.'
