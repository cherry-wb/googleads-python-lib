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

"""This example gets all mobile target platform ad unit sizes.

Tags: InventoryService.getAdUnitSizesByStatement
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


def main(client):
  # Initialize appropriate service.
  inventory_service = client.GetService('InventoryService', version='v201211')

  target_platform = 'MOBILE'

  # Create statement to select ad unit sizes available for the mobile platform.
  values = [{
      'key': 'targetPlatform',
      'value': {
          'xsi_type': 'TextValue',
          'value': target_platform
      }
  }]
  filter_statement = {'query': 'WHERE targetPlatform = :targetPlatform',
                      'values': values}

  # Get all ad unit sizes.
  ad_unit_sizes = inventory_service.GetAdUnitSizesByStatement(filter_statement)

  # Display results.
  for ad_unit_size in ad_unit_sizes:
    print ('Mobile ad unit size of dimension %s was found.' %
           ad_unit_size['fullDisplayString'])

  print
  print 'Number of ad unit sizes found: %s' % len(ad_unit_sizes)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
