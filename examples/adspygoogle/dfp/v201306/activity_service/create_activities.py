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

"""This code example creates new activities.

To determine which activities groups exist, run get_all_activities.py.

Tags: ActivityService.createActivities
"""

__author__ = 'Vincent Tsao'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils

# Set the ID of the activity group this activity is associated with.
ACTIVITY_GROUP_ID = 'INSERT_ACTIVITY_GROUP_ID_HERE'


def main(client, activity_group_id):
  # Initialize appropriate service.
  activity_service = client.GetService('ActivityService', version='v201306')

  # Create a daily visits activity.
  daily_visits_activity = {
      'name': 'Activity #%s' % Utils.GetUniqueName(),
      'activityGroupId': activity_group_id,
      'type': 'DAILY_VISITS'
  }

  # Create a custom activity.
  custom_activity = {
      'name': 'Activity #%s' % Utils.GetUniqueName(),
      'activityGroupId': activity_group_id,
      'type': 'CUSTOM'
  }

  # Create the activities on the server.
  activities = activity_service.CreateActivities([
      daily_visits_activity, custom_activity])

  # Display results.
  for activity in activities:
    print ('An activity with ID \'%s\', name \'%s\', and type \'%s\' was '
           'created.' % (activity['id'], activity['name'], activity['type']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ACTIVITY_GROUP_ID)
