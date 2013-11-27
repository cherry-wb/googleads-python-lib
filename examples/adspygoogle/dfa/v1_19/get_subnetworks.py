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

"""This example displays subnetwork names, IDs, and subnetwork IDs for a given
search string. Results are limited to 10.

Note that the permissions assigned to a subnetwork are not returned in a
human-readable format with this example. Run get_available_permissions.py to
see what permissions are available on a subnetwork.

Tags: subnetwork.getSubnetworks
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  subnetwork_service = client.GetSubnetworkService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Set subnetwork search criteria.
  subnetwork_search_criteria = {
      'pageSize': '10'
  }

  # Get subnetworks.
  results = subnetwork_service.GetSubnetworks(subnetwork_search_criteria)[0]

  # Display subnetwork names, IDs, and subnetwork IDs.
  if results['records']:
    for subnetwork in results['records']:
      print ('Subnetwork with name \'%s\', ID \'%s\', part of network ID \'%s\''
             ' was found.' % (subnetwork['name'], subnetwork['id'],
                              subnetwork['networkId']))
  else:
    print 'No subnetworks found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
