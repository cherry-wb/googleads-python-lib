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

"""This example gets all custom targeting keys and the values. To create custom
targeting keys and values, run create_custom_targeting_keys_and_values.py."""

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

filter_statement = {'query': 'LIMIT 500'}

# Get custom targeting keys by statement.
response = custom_targeting_service.GetCustomTargetingKeysByStatement(
    filter_statement)[0]
keys = []
if 'results' in response:
  keys = response['results']

# Display results.
if keys:
  key_ids = [key['id'] for key in keys]
  filter_statement = {'query': ('WHERE customTargetingKeyId IN (%s)'
                                % ', '.join(key_ids))}

  # Get custom targeting values by statement.
  response = custom_targeting_service.GetCustomTargetingValuesByStatement(
      filter_statement)[0]
  values = []
  if 'results' in response:
    values = response['results']

  # Create map of custom targeting key id to custom targeting values.
  key_value_map = {}
  for key in keys:
    for value in values:
      if key['id'] == value['customTargetingKeyId']:
        if key['id'] not in key_value_map.keys():
          key_value_map[key['id']] = []
        key_value_map[key['id']].append(value)
        break

  # Display results.
  for key in keys:
    print ('Custom targeting key with id \'%s\', name \'%s\', display name '
           '\'%s\', and type \'%s\' was found.'
           %(key['id'], key['name'], key['displayName'], key['type']))
    if key['id'] in key_value_map.keys():
      for value in key_value_map[key['id']]:
        print ('\tCustom targeting value with id \'%s\', name \'%s\', and '
               'display name \'%s\' was found.'
               % (value['id'], value['name'], value['displayName']))
else:
  print 'No keys were found.'
