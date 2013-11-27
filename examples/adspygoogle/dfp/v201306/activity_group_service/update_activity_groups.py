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

"""This code example updates activity groups.

To determine which activity groups exist, run get_all_activity_groups.py.

Tags: ActivityGroupService.getActivityGroup
Tags: ActivityGroupService.updateActivityGroups
"""

__author__ = 'Vincent Tsao'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the activity group and the company to update it with.
ACTIVITY_GROUP_ID = 'INSERT_ACTIVITY_GROUP_ID_HERE'
ADVERTISER_COMPANY_ID = 'INSERT_ADVERTISER_COMPANY_ID_HERE'


def main(client, activity_group_id, advertiser_company_id):
  # Initialize appropriate service.
  activity_group_service = client.GetService('ActivityGroupService',
                                             version='v201306')

  # Get the activity group.
  activity_group = activity_group_service.GetActivityGroup(activity_group_id)[0]

  # Update the companies.
  if activity_group:
    activity_group['companyIds'].append(advertiser_company_id)

    # Update the activity groups on the server.
    activity_groups = activity_group_service.UpdateActivityGroups([
        activity_group])

    # Display results.
    if activity_groups:
      for activity_group in activity_groups:
        print (('Activity group with ID \'%s\' and name \'%s\' was updated.')
               % (activity_group['id'], activity_group['name']))
    else:
      print 'No activity groups were updated.'
  else:
    print 'No activity groups found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ACTIVITY_GROUP_ID, ADVERTISER_COMPANY_ID)
