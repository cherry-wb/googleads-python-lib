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

"""This example creates a new activity group for a given spotlight
configuration. To get spotlight tag configuration, run get_advertisers.py.
To get activity types, run get_activity_types.py.

Tags: spotlight.saveSpotlightActivityGroup
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


SPOTLIGHT_CONFIGURATION_ID = 'INSERT_SPOTLIGHT_CONFIGURATION_ID_HERE'
ACTIVITY_TYPE = 'INSERT_ACTIVITY_TYPE_HERE'
GROUP_NAME = 'INSERT_GROUP_NAME_HERE'


def main(client, spotlight_configuration_id, activity_type, group_name):
  # Initialize appropriate service.
  spotlight_service = client.GetSpotlightService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Construct and save spotlight activity group.
  spotlight_activity_group = {
      'name': group_name,
      'spotlightConfigurationId': spotlight_configuration_id,
      'groupType': activity_type
  }
  result = spotlight_service.SaveSpotlightActivityGroup(
      spotlight_activity_group)[0]

  # Display results.
  print 'Spotlight activity group with ID \'%s\' was created.' % result['id']


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, SPOTLIGHT_CONFIGURATION_ID, ACTIVITY_TYPE, GROUP_NAME)
