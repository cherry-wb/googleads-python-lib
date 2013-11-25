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

"""This example gets all user team associations.

To create user team associations, run create_user_team_assocations.py.

Tags: UserTeamAssociationService.getUserTeamAssociationsByStatement
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
user_team_association_service = client.GetService(
    'UserTeamAssociationService', version='v201208')

# Get the user team associations by statement.
user_team_associations = DfpUtils.GetAllEntitiesByStatementWithService(
    user_team_association_service)

# Display results.
for user_team_association in user_team_associations:
  print ('User team association between user with ID \'%s\' and team with ID '
         '\'%s\' was found.' % (user_team_association['userId'],
                                user_team_association['teamId']))

print
print 'Number of results found: %s' % len(user_team_associations)
