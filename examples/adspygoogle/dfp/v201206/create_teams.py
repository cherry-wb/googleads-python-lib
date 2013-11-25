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

"""This example creates new teams.

To determine which teams exist, run get_all_teams.py.

Tags: TeamService.createTeams
"""

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
team_service = client.GetService('TeamService', version='v201206')

# Create team objects.
teams = []
for i in xrange(5):
  team = {
      'name': 'Team #%d' % i,
      'hasAllCompanies': 'false',
      'hasAllInventory': 'false'
  }
  teams.append(team)

# Add Teams.
teams = team_service.CreateTeams(teams)

# Display results.
for team in teams:
  print ('Team with ID \'%s\' and name \'%s\' was created.'
         % (team['id'], team['name']))
