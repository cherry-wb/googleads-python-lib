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

"""This code example gets all web target platform ad unit sizes."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
inventory_service = client.GetService(
    'InventoryService', 'https://www.google.com', 'v201203')

target_platform = 'WEB'

# Create statement object to only select web ad unit sizes.
values = [{
    'key': 'targetPlatform',
    'value': {
        'xsi_type': 'TextValue',
        'value': target_platform
    }
}]
filter_statement = {'query': 'WHERE targetPlatform = :targetPlatform',
                    'values': values}

# Get ad unit sizes.
ad_unit_sizes = inventory_service.GetAdUnitSizesByStatement(filter_statement)

# Display results.
for ad_unit_size in ad_unit_sizes:
  print 'Web ad unit size of dimension %s x %s found.' % (
      ad_unit_size['size']['width'], ad_unit_size['size']['height'])

print
print 'Number of results found: %s' % len(ad_unit_sizes)
