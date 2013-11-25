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

"""This code example updates teams by adding you to them, up to the first 500.
To determine which teams exist, run get_all_teams.py."""

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
team_service = client.GetService(
    'TeamService', 'https://www.google.com', 'v201203')

user_service = client.GetService(
    'UserService', 'https://www.google.com', 'v201203')

# Get current user's ID.
user_id = user_service.GetCurrentUser()[0]['id']

# Create a statement to select first 500 teams.
filter_statement = {'query': 'LIMIT 500'}

# Get teams by filter.
response = team_service.GetTeamsByStatement(filter_statement)[0]
teams = []
if 'results' in response:
  teams = response['results']

if teams:
  updated_teams = []
  for team in teams:
    if user_id not in team['userIds']:
      team['userIds'].append(user_id)
      updated_teams.append(team)

  # Update teams remotely.
  teams = team_service.UpdateTeams(updated_teams)

  # Display results.
  if teams:
    for team in teams:
      print ('Team with id \'%s\' and name \'%s\' was updated.'
             % (team['id'], team['name']))
  else:
    print 'No teams were updated.'
else:
  print 'No teams found to update.'
