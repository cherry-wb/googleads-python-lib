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

"""This code example gets all child ad units of the effective root ad unit.

To create ad units, run create_ad_units.py

Tags: InventoryService.getAdUnitsByStatement
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
  inventory_service = client.GetService('InventoryService', version='v201208')
  network_service = client.GetService('NetworkService', version='v201208')

  root_id = network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']

  # Create a statement to select the children of the effective root ad unit.
  values = [{
      'key': 'id',
      'value': {
          'xsi_type': 'TextValue',
          'value': root_id
      }
  }]
  query = 'WHERE parentId = :id'

  # Get ad units by statement.
  ad_units = DfpUtils.GetAllEntitiesByStatementWithService(
      inventory_service, query=query, bind_vars=values)

  # Display results.
  for ad_unit in ad_units:
    print ('Ad unit with ID \'%s\' and name \'%s\' was found.'
           % (ad_unit['id'], ad_unit['name']))

  print
  print 'Number of results found: %s' % len(ad_units)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
