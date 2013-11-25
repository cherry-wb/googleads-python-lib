#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""This example retrieves available creative field values for a given string and
displays the names and IDs.

Tags: creativefield.getCreativeFieldValues
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


CREATIVE_FIELD_ID = 'INSERT_CREATIVE_FIELD_ID_HERE'


def main(client, creative_field_id):
  # Initialize appropriate service.
  creative_field_service = client.GetCreativeFieldService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Set up creative field value search criteria structure.
  creative_field_value_search_criteria = {
      'creativeFieldIds': [creative_field_id],
      'pageSize': '10'
  }

  # Get creative field values for the selected criteria.
  results = creative_field_service.GetCreativeFieldValues(
      creative_field_value_search_criteria)[0]

  # Display creative field value names and IDs.
  if results['records']:
    for creative_field_value in results['records']:
      print ('Creative field value with name \'%s\' and ID \'%s\' was found.'
             % (creative_field_value['name'], creative_field_value['id']))
  else:
    print 'No creative field values found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, CREATIVE_FIELD_ID)
