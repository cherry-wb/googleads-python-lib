#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""This code example gets all active activities.

To create activities, run create_activities.py.

Tags: ActivityService.getActivitiesByStatement
"""

__author__ = 'Vincent Tsao'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

# Set the ID of the activity group these activities are associated with.
ACTIVITY_GROUP_ID = 'INSERT_ACTIVITY_GROUP_ID_HERE'


def main(client, activity_group_id):
  # Initialize appropriate service.
  activity_service = client.GetService('ActivityService', version='v201302')

  # Create statement object to only select active activities.
  values = [
      {
          'key': 'activityGroupId',
          'value': {
              'xsi_type': 'NumberValue',
              'value': activity_group_id
          }
      },
      {
          'key': 'status',
          'value': {
              'xsi_type': 'TextValue',
              'value': 'ACTIVE'
          }

      }
  ]
  query = 'WHERE activityGroupId = :activityGroupId and status = :status'

  # Get activities by statement.
  activities = DfpUtils.GetAllEntitiesByStatementWithService(
      activity_service, query=query, bind_vars=values)

  # Display results.
  for activity in activities:
    print ('Activity with ID \'%s\', name \'%s\', and type \'%s\' was '
           'found.' % (activity['id'], activity['name'], activity['type']))

  print
  print 'Number of results found: %s' % len(activities)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ACTIVITY_GROUP_ID)
