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

"""This code example updates ad unit sizes by adding a banner ad size.

To determine which ad units exist, run get_all_ad_units.py.

Tags: InventoryService.getAdUnit
Tags: InventoryService.updateAdUnits
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the ad unit to get.
AD_UNIT_ID = 'INSERT_AD_UNIT_ID_HERE'


def main(client, ad_unit_id):
  # Initialize appropriate service.
  inventory_service = client.GetService('InventoryService', version='v201211')

  # Get the ad units.
  ad_unit = inventory_service.GetAdUnit(ad_unit_id)[0]

  # Add the size 468x60 to the ad unit.
  ad_unit_size = {
      'size': {
          'width': '468',
          'height': '60'
      },
      'environmentType': 'BROWSER'
  }
  if 'adUnitSizes' not in ad_unit:
    ad_unit['adUnitSizes'] = []
  ad_unit['adUnitSizes'].append(ad_unit_size)

  # Update ad unit on the server.
  ad_units = inventory_service.UpdateAdUnits([ad_unit])

  # Display results.
  for ad_unit in ad_units:
    ad_unit_sizes = ['{%s x %s}' % (size['size']['width'],
                                    size['size']['height'])
                     for size in ad_unit['adUnitSizes']]
    print ('Ad unit with ID \'%s\', name \'%s\', and sizes [%s] was updated'
           % (ad_unit['id'], ad_unit['name'], ','.join(ad_unit_sizes)))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, AD_UNIT_ID)
