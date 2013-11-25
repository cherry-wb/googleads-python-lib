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

"""This example sets custom field values on a line item.

To determine which custom fields exist, run get_all_custom_fields.py.
To determine which line item exist, run get_all_line_items.py.
To create custom field options, run create_custom_field_options.py

Tags: CustomFieldService.getCustomField
Tags: LineItemService.getLineItem
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the custom fields, custom field option, and line item.
CUSTOM_FIELD_ID = 'INSERT_STRING_CUSTOM_FIELD_ID_HERE'
DROP_DOWN_CUSTOM_FIELD_ID = 'INSERT_DROP_DOWN_CUSTOM_FIELD_ID_HERE'
CUSTOM_FIELD_OPTION_ID = 'INSERT_CUSTOM_FIELD_OPTION_ID_HERE'
LINE_ITEM_ID = 'INSERT_LINE_ITEM_ID_HERE'


def main(client, custom_field_id, drop_down_custom_field_id,
         custom_field_option_id, line_item_id):
  # Initialize appropriate services.
  custom_field_service = client.GetService(
      'CustomFieldService', version='v201211')

  line_item_service = client.GetService('LineItemService', version='v201211')

  # Get custom field.
  custom_field = custom_field_service.GetCustomField(custom_field_id)[0]

  # Get drop-down custom field.
  drop_down_custom_field = custom_field_service.GetCustomField(
      drop_down_custom_field_id)[0]

  # Get line item.
  line_item = line_item_service.GetLineItem(line_item_id)[0]

  if custom_field and line_item:
    # Create custom field values.
    custom_field_value = {
        'customFieldId': custom_field['id'],
        'type': 'CustomFieldValue',
        'value': {
            'type': 'TextValue',
            'value': 'Custom field value'
        }
    }

    drop_down_custom_field_value = {
        'customFieldId': drop_down_custom_field['id'],
        'type': 'DropDownCustomFieldValue',
        'customFieldOptionId': custom_field_option_id,
    }

    custom_field_values = [custom_field_value, drop_down_custom_field_value]

    old_custom_field_values = []
    if 'customFieldValues' in line_item:
      old_custom_field_values = line_item['customFieldValues']

    # Only add existing custom field values for different custom fields than the
    # ones you are setting.
    for old_custom_field_value in old_custom_field_values:
      if (old_custom_field_value['customFieldId'] != custom_field_value['id']
          and old_custom_field_value['customFieldId'] !=
          drop_down_custom_field_value['id']):
        custom_field_values.append(old_custom_field_value)

    line_item['customFieldValues'] = custom_field_values

    # Update the line item on the server.
    line_items = line_item_service.UpdateLineItems([line_item])

    # Display results.
    if line_items:
      for line_item in line_items:
        custom_field_value_strings = []
        for value in line_item['customFieldValues']:
          if value['BaseCustomFieldValue_Type'] == 'CustomFieldValue':
            custom_field_value_string = (
                '{ID: \'%s\', value: \'%s\'}'
                % (value['customFieldId'], value['value']['value']))
          elif value['BaseCustomFieldValue_Type'] == 'DropDownCustomFieldValue':
            custom_field_value_string = (
                '{ID: \'%s\', custom field option ID: \'%s\'}'
                % (value['customFieldId'], value['customFieldOptionId']))
          custom_field_value_strings.append(custom_field_value_string)
        print ('Line item with ID \'%s\' set with custom field values %s.'
               % (line_item['id'], ','.join(custom_field_value_strings)))
    else:
      print 'No line items were updated.'
  else:
    print 'Line item or custom field not found.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CUSTOM_FIELD_ID, DROP_DOWN_CUSTOM_FIELD_ID,
       CUSTOM_FIELD_OPTION_ID, LINE_ITEM_ID)
