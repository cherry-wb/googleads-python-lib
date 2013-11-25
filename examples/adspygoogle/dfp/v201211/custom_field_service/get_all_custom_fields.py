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

"""This example gets all custom fields.

To create custom fields, run create_custom_fields.py.

Tags: CustomFieldService.getCustomFieldsByStatement
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


def main(client):
  # Initialize appropriate service.
  custom_field_service = client.GetService(
      'CustomFieldService', version='v201211')

  # Get custom fields by statement.
  custom_fields = DfpUtils.GetAllEntitiesByStatementWithService(
      custom_field_service)

  # Display results.
  for custom_field in custom_fields:
    if custom_field['CustomField_Type'] == 'DropDownCustomField':
      drop_down_custom_field_strings = []
      if 'options' in custom_field:
        drop_down_custom_field_strings = [custom_field_option['displayName']
                                          for custom_field_option
                                          in custom_field['options']]
      print ('Drop-down custom field with ID \'%s\', name \'%s\', and options '
             '{%s} was found.' % (custom_field['id'], custom_field['name'],
                                  ','.join(drop_down_custom_field_strings)))
    else:
      print ('Custom field with ID \'%s\' and name \'%s\' was found'
             % (custom_field['id'], custom_field['name']))
  print
  print 'Number of results found: %s' % len(custom_fields)


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
