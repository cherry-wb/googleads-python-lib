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

"""This code example updates activities.

To determine which activities exist, run get_all_activities.py.

Tags: ActivityService.getActivity
Tags: ActivityService.updateActivities
"""

__author__ = 'Vincent Tsao'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the activity to update.
ACTIVITY_ID = 'INSERT_ACTIVITY_ID_HERE'


def main(client, activity_id):
  # Initialize appropriate service.
  activity_service = client.GetService('ActivityService', version='v201302')

  # Get the activity.
  activity = activity_service.GetActivity(activity_id)[0]

  if activity:
    # Update the expected URL.
    activity['expectedURL'] = 'https://google.com'

    # Update the activity on the server.
    activities = activity_service.UpdateActivities([activity])

    # Display results.
    if activities:
      for updated_activity in activities:
        print (('Activity with ID \'%s\' and name \'%s\' was updated.')
               % (updated_activity['id'], updated_activity['name']))
    else:
      print 'No activities were updated.'
  else:
    print 'No activities found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ACTIVITY_ID)
