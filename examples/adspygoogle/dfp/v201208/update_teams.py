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

"""This example updates teams by adding an ad unit to the first 5.

To determine which teams exist, run get_all_teams.py. To determine which ad
units exist, run get_all_ad_units.py

Tags: TeamService.getTeamsByStatement, TeamService.updateTeams
"""

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
team_service = client.GetService('TeamService', version='v201208')

# Set the ID of the ad unit to add to the teams.
ad_unit_id = 'INSERT_AD_UNIT_ID_HERE'

# Create a statement to select first 5 teams that aren't built-in.
filter_statement = {'query': 'WHERE id > 0 LIMIT 5'}

# Get teams by statement.
response = team_service.GetTeamsByStatement(filter_statement)[0]
teams = []
if 'results' in response:
  teams = response['results']

if teams:
  # Update each local team object by adding the ad unit to it.
  for team in teams:
    ad_unit_ids = []
    if 'adUnitIds' in team:
      ad_unit_ids = team['adUnitIds']
    # Don't add the ad unit if the team has all inventory already.
    if not Utils.BoolTypeConvert(team['hasAllInventory']):
      ad_unit_ids.append(ad_unit_id)
    team['adUnitIds'] = ad_unit_ids

  # Update teams on the server.
  teams = team_service.UpdateTeams(teams)

  # Display results.
  if teams:
    for team in teams:
      print ('Team with id \'%s\' and name \'%s\' was updated.'
             % (team['id'], team['name']))
  else:
    print 'No teams were updated.'
else:
  print 'No teams found to update.'
