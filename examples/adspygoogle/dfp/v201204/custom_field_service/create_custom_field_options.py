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

"""This example creates custom field options for a drop-down custom field.

Once created, custom field options can be found under the options fields of the
drop-down custom field and they cannot be deleted. To determine which custom
fields exist, run get_all_custom_fields.py.

Tags: CustomFieldService.createCustomFieldOptions
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the drop-down custom field to create options for.
CUSTOM_FIELD_ID = 'INSERT_DROP_DOWN_CUSTOM_FIELD_ID_HERE'


def main(client, custom_field_id):
  # Initialize appropriate service.
  custom_field_service = client.GetService(
      'CustomFieldService', version='v201204')

  # Create custom field options.
  custom_field_options = [
      {
          'displayName': 'Approved',
          'customFieldId': custom_field_id
      },
      {
          'displayName': 'Unapproved',
          'customFieldId': custom_field_id
      }
  ]

  # Add custom field options.
  custom_field_options = custom_field_service.CreateCustomFieldOptions(
      custom_field_options)

  # Display results.
  for custom_field_option in custom_field_options:
    print ('Custom field option with ID \'%s\' and name \'%s\' was created.'
           % (custom_field_option['id'], custom_field_option['displayName']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CUSTOM_FIELD_ID)
