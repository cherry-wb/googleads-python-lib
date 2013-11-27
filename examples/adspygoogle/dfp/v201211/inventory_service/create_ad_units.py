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

"""This code example creates new ad units.

To determine which ad units exist, run get_all_ad_units.py

Tags: InventoryService.createAdUnits
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


def main(client, parent_id):
  # Initialize appropriate service.
  inventory_service = client.GetService('InventoryService', version='v201211')

  # Create ad unit size.
  ad_unit_size = {
      'size': {
          'width': '300',
          'height': '250'
      },
      'environmentType': 'BROWSER'
  }

  # Create ad unit objects.
  web_ad_unit = {
      'name': 'Web_ad_unit_%s' % Utils.GetUniqueName(),
      'parentId': parent_id,
      'description': 'Web ad unit description.',
      'targetWindow': 'BLANK',
      'targetPlatform': 'WEB',
      'adUnitSizes': [ad_unit_size]
  }

  mobile_ad_unit = {
      'name': 'Mobile_ad_unit_%s' % Utils.GetUniqueName(),
      'parentId': parent_id,
      'description': 'Mobile ad unit description.',
      'targetWindow': 'BLANK',
      'targetPlatform': 'MOBILE',
      'mobilePlatform': 'APPLICATION',
      'adUnitSizes': [ad_unit_size]
  }

  # Add ad units.
  ad_units = inventory_service.CreateAdUnits([web_ad_unit, mobile_ad_unit])

  # Display results.
  for ad_unit in ad_units:
    print ('Ad unit with ID \'%s\', name \'%s\', and target platform \'%s\' '
           'was created.' % (ad_unit['id'], ad_unit['name'],
                             ad_unit['targetPlatform']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

  # Get the Network Service.
  network_service = dfp_client.GetService('NetworkService', version='v201211')

  # Set the parent ad unit's ID for all ad units to be created under.
  parent_id = network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']
  main(dfp_client, parent_id)
