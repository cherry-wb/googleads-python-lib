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

"""This code example gets all active creative wrappers.

To create creative wrappers, run create_creative_wrappers.py.

Tags: CreativeWrapperService.getCreativeWrappersByStatement
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
  creative_wrapper_service = client.GetService('CreativeWrapperService',
                                               version='v201302')

  # Create statement object to only select active creative wrappers.
  values = [{
      'key': 'status',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'ACTIVE'
      }
  }]
  query = 'WHERE status = :status'

  # Get creative_wrappers by statement.
  creative_wrappers = DfpUtils.GetAllEntitiesByStatementWithService(
      creative_wrapper_service, query=query, bind_vars=values)

  # Display results.
  for creative_wrapper in creative_wrappers:
    print ('Creative wrapper with ID \'%s\' applying to label \'%s\' with '
           'status \'%s\' was found.' % (creative_wrapper['id'],
                                         creative_wrapper['labelId'],
                                         creative_wrapper['status']))

  print
  print 'Number of results found: %s' % len(creative_wrappers)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
