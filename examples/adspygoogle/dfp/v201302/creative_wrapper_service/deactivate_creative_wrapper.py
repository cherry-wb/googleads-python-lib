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

"""This code example deactivates a creative wrapper belonging to a label.

Tags: CreativeWrapperService.getCreativeWrapperByStatement
Tags: CreativeWrapperService.performCreativeWrapperAction
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

LABEL_ID = 'INSERT_LABEL_ID_HERE'


def main(client, label_id):
  # Initialize appropriate service.
  creative_wrapper_service = client.GetService('CreativeWrapperService',
                                               version='v201302')

  # Create a query to select the active creative wrappers for the given label.
  values = [{
      'key': 'labelId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': label_id
      }
  }, {
      'key': 'status',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'ACTIVE'
      }
  }]

  query = 'WHERE status = :status AND labelId = :labelId'

  # Get creative wrapper by statement.
  creative_wrappers = DfpUtils.GetAllEntitiesByStatementWithService(
      creative_wrapper_service, query=query, bind_vars=values)
  for creative_wrapper in creative_wrappers:
    print ('Creative wrapper with ID \'%s\' applying to label \'%s\' with '
           'status \'%s\' will be deactivated.' % (creative_wrapper['id'],
                                                   creative_wrapper['labelId'],
                                                   creative_wrapper['status']))
  print ('Number of creative wrappers to be deactivated: %s'
         % len(creative_wrappers))

  # Perform action.
  result = creative_wrapper_service.PerformCreativeWrapperAction(
      {'type': 'DeactivateCreativeWrappers'},
      {'query': query, 'values': values})[0]

  # Display results.
  if result and int(result['numChanges']) > 0:
    print 'Number of creative wrappers deactivated: %s' % result['numChanges']
  else:
    print 'No creative wrappers were deactivated.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(dfp_client, LABEL_ID)
