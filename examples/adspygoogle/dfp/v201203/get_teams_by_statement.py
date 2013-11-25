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

"""This example gets all teams that you belong to. The statement retrieves up to
the maximum page size limit of 500. To create a team, run create_team.py."""

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

# Get current user's teams.
team_ids = user_service.GetCurrentUser()[0]['teamIds']

# Create a statement to only select teams by their IDs.
filter_statement = {'query': 'WHERE id IN (%s) LIMIT 500' % ','.join(team_ids)}

# Get teams by statement.
response = team_service.GetTeamsByStatement(filter_statement)[0]
teams = []
if 'results' in response:
  teams = response['results']

# Display results.
for team in teams:
  print ('Team with id \'%s\' and name \'%s\' was found.'
         % (team['id'], team['name']))

print
print 'Number of results found: %s' % len(teams)
