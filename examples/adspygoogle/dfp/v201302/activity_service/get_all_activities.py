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

"""This code example gets all activities.

To create activities, run create_activities.py.

Tags: ActivityService.getActivitiesByStatement
Tags: ActivityGroupService.getActivityGroupsByStatement
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


def GetAllActivityGroupIds(client):
  """Gets all activity group IDs."""

  activity_group_ids = []

  # Initialize appropriate service.
  activity_group_service = client.GetService('ActivityGroupService',
                                             version='v201302')

  # Get activity groups by statement.
  activity_groups = DfpUtils.GetAllEntitiesByStatementWithService(
      activity_group_service)

  # Display results.
  for activity_group in activity_groups:
    activity_group_ids.append(activity_group['id'])

  return activity_group_ids


def main(client):
  # Initialize appropriate service.
  activity_service = client.GetService('ActivityService', version='v201302')

  total_results_counter = 0

  activity_group_ids = GetAllActivityGroupIds(client)

  for activity_group_id in activity_group_ids:
    # Set the activity group ID to select from.
    values = [{
        'key': 'activityGroupId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': activity_group_id
        }
    }]
    query = 'WHERE activityGroupId = :activityGroupId'

    # Get activities by statement.
    activities = DfpUtils.GetAllEntitiesByStatementWithService(
        activity_service, query=query, bind_vars=values)

    total_results_counter += len(activities)

    # Display results.
    for activity in activities:
      print ('Activity with ID \'%s\', name \'%s\', and type \'%s\' was '
             'found.' % (activity['id'], activity['name'], activity['type']))

  print
  print 'Number of results found: %s' % total_results_counter


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
