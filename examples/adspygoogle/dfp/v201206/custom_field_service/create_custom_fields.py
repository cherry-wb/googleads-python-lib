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

"""This example creates custom fields.

To determine which custom fields exist, run get_all_custom_fields.py.

Tags: CustomFieldService.createCustomFields
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


def main(client):
  # Initialize appropriate service.
  custom_field_service = client.GetService(
      'CustomFieldService', version='v201206')

  # Create custom field objects.
  custom_fields = [
      {
          'name': 'Customer comments #%s' % Utils.GetUniqueName(),
          'entityType': 'LINE_ITEM',
          'dataType': 'STRING',
          'visibility': 'FULL'
      }, {
          'name': 'Internal approval status #%s' % Utils.GetUniqueName(),
          'entityType': 'LINE_ITEM',
          'dataType': 'DROP_DOWN',
          'visibility': 'FULL'
      }
  ]

  # Add custom fields.
  custom_fields = custom_field_service.CreateCustomFields(custom_fields)

  # Display results.
  for custom_field in custom_fields:
    print ('Custom field with ID \'%s\' and name \'%s\' was created.'
           % (custom_field['id'], custom_field['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
