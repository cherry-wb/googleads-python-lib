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

"""This code example gets all creative sets.

To create creative sets, run create_creative_sets.py.

Tags: CreativeSetService.getCreativeSetsByStatement
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


def main(client):
  # Initialize appropriate service.
  creative_set_service = client.GetService('CreativeSetService',
                                           version='v201208')

  # Get creative sets by statement.
  creative_sets = DfpUtils.GetAllEntitiesByStatementWithService(
      creative_set_service)

  # Display results.
  for creative_set in creative_sets:
    print (('Creative set with ID \'%s\', master creative ID \'%s\', and '
            'companion creative IDs {%s} was found.')
           % (creative_set['id'], creative_set['masterCreativeId'],
              ','.join(creative_set['companionCreativeIds'])))

  print
  print 'Number of results found: %s' % len(creative_sets)


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
