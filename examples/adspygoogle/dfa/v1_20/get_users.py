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

"""This example displays user name, ID, network ID, subnetwork ID, and user
group ID for the given search criteria. Results are limited to the first 10
records.

Tags: user.getUsersByCriteria
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  user_service = client.GetUserService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Set user search criteria.
  user_search_criteria = {
      'pageSize': '10'
  }

  # Get users that match the search criteria.
  results = user_service.GetUsersByCriteria(user_search_criteria)[0]

  # Display user names, IDs, network IDs, subnetwork IDs, and group IDs.
  if results['records']:
    for user in results['records']:
      print ('User with name \'%s\', ID \'%s\', network ID \'%s\', '
             'subnetwork ID \'%s\', and user role id \'%s\' was found.'
             % (user['name'], user['id'], user['networkId'],
                user['subnetworkId'], user['userGroupId']))
  else:
    print 'No users found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
