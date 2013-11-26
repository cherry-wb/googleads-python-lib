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

"""This example displays available placements for a given search string. Results
are limited to 10.

Tags: placement.getPlacementsByCriteria
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  placement_service = client.GetPlacementService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Set placement search criteria.
  placement_search_criteria = {
      'pageSize': '10'
  }

  # Get placement types.
  results = placement_service.GetPlacementsByCriteria(
      placement_search_criteria)[0]

  # Display placement names and IDs.
  if results['records']:
    for placement in results['records']:
      print ('Placement with name \'%s\' and ID \'%s\' was found.'
             % (placement['name'], placement['id']))
  else:
    print 'No placements found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
