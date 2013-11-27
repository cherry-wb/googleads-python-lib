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

"""This code example creates new activity groups.

To determine which activity groups exist, run get_all_activity_groups.py.

Tags: ActivityGroupService.createActivityGroups
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

# Set the ID of the advertiser company this activity group is associated with.
ADVERTISER_COMPANY_ID = 'INSERT_ADVERTISER_COMPANY_ID_HERE'


def main(client, advertiser_company_id):
  # Initialize appropriate service.
  activity_group_service = client.GetService('ActivityGroupService',
                                             version='v201302')

  # Create a short-term activity group.
  short_term_activity_group = {
      'name': 'Short-term activity group #%s' % Utils.GetUniqueName(),
      'companyIds': [advertiser_company_id],
      'clicksLookback': '1',
      'impressionsLookback': '1'
  }

  # Create a long-term activity group.
  long_term_activity_group = {
      'name': 'Long-term activity group #%s' % Utils.GetUniqueName(),
      'companyIds': [advertiser_company_id],
      'clicksLookback': '30',
      'impressionsLookback': '30'
  }

  # Create the activity groups on the server.
  activity_groups = activity_group_service.CreateActivityGroups([
      short_term_activity_group, long_term_activity_group])

  # Display results.
  for activity_group in activity_groups:
    print ('Activity group with ID \'%s\' and name \'%s\' was created.'
           % (activity_group['id'], activity_group['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ADVERTISER_COMPANY_ID)
