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

"""This example updates a line item to add custom criteria targeting. To
determine which line items exist, run get_all_line_items.py. To determine which
custom targeting keys and values exist, run
get_all_custom_targeting_keys_and_values.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import pprint
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
line_item_service = client.GetService('LineItemService', version='v201204')

line_item_id = 'INSERT_LINE_ITEM_ID_HERE'
key_id1 = 'INSERT_TARGETING_KEY_ID_HERE'
key_id2 = 'INSERT_TARGETING_KEY_ID_HERE'
key_id3 = 'INSERT_TARGETING_KEY_ID_HERE'

value_id1 = 'INSERT_TARGETING_VALUE_ID_HERE'
value_id2 = 'INSERT_TARGETING_VALUE_ID_HERE'
value_id3 = 'INSERT_TARGETING_VALUE_ID_HERE'

# create custom criterias
custom_criteria1 = {
    'xsi_type': 'CustomCriteria',
    'keyId': key_id1,
    'valueIds': [value_id1],
    'operator': 'IS'
}

custom_criteria2 = {
    'xsi_type': 'CustomCriteria',
    'keyId': key_id2,
    'valueIds': [value_id2],
    'operator': 'IS_NOT'
}

custom_criteria3 = {
    'xsi_type': 'CustomCriteria',
    'keyId': key_id3,
    'valueIds': [value_id3],
    'operator': 'IS'
}

# Create the custom criteria set that will resemble:
# (custom_criteria1.key == custom_criteria1.value OR
#  (custom_criteria2.key != custom_criteria2.value AND
#   custom_criteria13.key == custom_criteria3.value))
sub_set = {
    'xsi_type': 'CustomCriteriaSet',
    'logicalOperator': 'AND',
    'children': [custom_criteria2, custom_criteria3]
}

top_set = {
    'xsi_type': 'CustomCriteriaSet',
    'logicalOperator': 'OR',
    'children': [custom_criteria1, sub_set]
}

# Set custom criteria targeting on the line item.
line_item = line_item_service.GetLineItem(line_item_id)[0]
line_item['targeting']['customTargeting'] = top_set

# Update line item.
line_item = line_item_service.UpdateLineItem(line_item)[0]

# Display results.
if line_item:
  print ('Line item with id \'%s\' updated with custom criteria targeting:'
         % line_item['id'])
  pprint.pprint(line_item['targeting']['customTargeting'])
else:
  print 'No line items were updated.'
