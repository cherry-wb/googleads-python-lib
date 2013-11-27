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

"""This code example updates a creative set by adding a companion creative.

To determine which creative sets exist, run get_all_creative_sets.py.

Tags: CreativeSetService.updateCreativeSet
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the creative set to get.
CREATIVE_SET_ID = 'INSERT_CREATIVE_SET_ID_HERE'
COMPANION_CREATIVE_ID = 'INSERT_COMPANION_CREATIVE_ID_HERE'


def main(client, creative_set_id, companion_creative_id):
  # Initialize appropriate service.
  creative_set_service = client.GetService('CreativeSetService',
                                           version='v201208')

  # Get creative set.
  creative_set = creative_set_service.GetCreativeSet(creative_set_id)[0]

  creative_set['companionCreativeIds'].append(companion_creative_id)

  # Update the creative sets on the server.
  creative_set = creative_set_service.UpdateCreativeSet(creative_set)[0]

  # Display results.
  print (('Creative set with ID \'%s\', master creative ID \'%s\', and '
          'companion creative IDs {%s} was updated.')
         % (creative_set['id'], creative_set['masterCreativeId'],
            ','.join(creative_set['companionCreativeIds'])))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CREATIVE_SET_ID, COMPANION_CREATIVE_ID)
