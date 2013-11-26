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

"""This example displays activity method type names and IDs.

Tags: spotlight.getSpotlightTagMethodTypes
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  spotlight_service = client.GetSpotlightService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Get method types.
  results = spotlight_service.GetSpotlightTagMethodTypes()

  # Display method type names and IDs.
  if results:
    for method_type in results:
      print ('Method type with name \'%s\' and ID \'%s\' was found.'
             % (method_type['name'], method_type['id']))
  else:
    print 'No method types found.'


if __name__ == '__main__':
  # Initialize client object. This example shows you how to put authentication
  # information into a client at initialization.
  client = DfaClient({'Username': 'INSERT_USER_NAME_HERE',
                      'Password': 'INSERT_PASSWORD_HERE'})
  main(client)
