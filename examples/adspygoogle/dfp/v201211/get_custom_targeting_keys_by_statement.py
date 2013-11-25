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

"""This example gets all predefined custom targeting keys. The statement
retrieves up to the maximum page size limit of 500. To create custom
targeting keys, run create_custom_targeting_keys_and_values.py."""

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
    'CustomTargetingService', version='v201211')

values = [{
    'key': 'type',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'PREDEFINED'
    }
}]
filter_statement = {'query': 'WHERE type = :type LIMIT 500',
                    'values': values}

# Get custom targeting keys by statement.
response = custom_targeting_service.GetCustomTargetingKeysByStatement(
    filter_statement)[0]
keys = []
if 'results' in response:
  keys = response['results']

# Display results.
if keys:
  for key in keys:
    print ('Custom targeting key with id \'%s\', name \'%s\', display name '
           '\'%s\', and type \'%s\' was found.'
           % (key['id'], key['name'], key['displayName'], key['type']))
else:
  print 'No keys were found.'
