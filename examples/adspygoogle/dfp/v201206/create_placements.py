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

"""This code example creates new placements for various ad unit sizes. To
determine which placements exist, run get_all_placements.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
placement_service = client.GetService('PlacementService', version='v201206')
inventory_service = client.GetService('InventoryService', version='v201206')

# Create placement object to store medium rectangle ad units.
medium_rectangle_ad_unit_placement = {
    'name': 'Medium rectangle AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 300x250',
    'targetedAdUnitIds': []
}

# Create placement object to store skyscraper ad units.
skyscraper_ad_unit_placement = {
    'name': 'Skyscraper AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 120x600',
    'targetedAdUnitIds': []
}

# Create placement object to store banner ad units.
banner_ad_unit_placement = {
    'name': 'Banner AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 468x60',
    'targetedAdUnitIds': []
}

placement_list = []

# Get the first 500 ad units.
filter_statement = {'query': 'LIMIT 500'}
response = inventory_service.GetAdUnitsByStatement(filter_statement)[0]
ad_units = []
if 'results' in response:
  ad_units = response['results']

# Separate the ad units by size.
for ad_unit in ad_units:
  if 'adUnitSizes' in ad_unit:
    for ad_unit_size in ad_unit['adUnitSizes']:
      size = ad_unit_size['size']
      if size['width'] == '300' and size['height'] == '250':
        medium_rectangle_ad_unit_placement['targetedAdUnitIds'].append(
            ad_unit['id'])
      elif size['width'] == '120' and size['height'] == '600':
        skyscraper_ad_unit_placement['targetedAdUnitIds'].append(ad_unit['id'])
      elif size['width'] == '468' and size['height'] == '60':
        banner_ad_unit_placement['targetedAdUnitIds'].append(ad_unit['id'])

# Only create placements with one or more ad unit.
if len(medium_rectangle_ad_unit_placement['targetedAdUnitIds']):
  placement_list.append(medium_rectangle_ad_unit_placement)

if len(skyscraper_ad_unit_placement['targetedAdUnitIds']):
  placement_list.append(skyscraper_ad_unit_placement)

if len(banner_ad_unit_placement['targetedAdUnitIds']):
  placement_list.append(banner_ad_unit_placement)

# Add placements.
placements = placement_service.CreatePlacements(placement_list)

# Display results.
for placement in placements:
  ad_unit_ids = ''
  if 'targetedAdUnitIds' in placement:
    ad_unit_ids = ', '.join(placement['targetedAdUnitIds'])
  print ('A Placement with ID \'%s\', name \'%s\', and containing ad units '
         '{%s} was created.' % (placement['id'], placement['name'],
                                ad_unit_ids))
