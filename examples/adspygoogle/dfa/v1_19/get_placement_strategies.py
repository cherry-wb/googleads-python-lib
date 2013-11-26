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

"""This example displays available placement strategies for a given search
string. Results are limited to 10.

Tags: strategy.getPlacementStrategiesByCriteria
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  placement_strategy_service = client.GetStrategyService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Create placement strategy search criteria structure.
  placement_strategy_search_criteria = {
      'pageSize': '10'
  }

  # Get placement strategy record set.
  results = placement_strategy_service.GetPlacementStrategiesByCriteria(
      placement_strategy_search_criteria)[0]

  # Display placement strategy names, IDs and descriptions.
  if results['records']:
    for placement in results['records']:
      print ('Placement strategy with name \'%s\' and ID \'%s\' was found.'
             % (placement['name'], placement['id']))
  else:
    print 'No placement strategies found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
