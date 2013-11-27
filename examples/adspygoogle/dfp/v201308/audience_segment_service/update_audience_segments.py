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

"""This example updates rule based first party audience segments.

To determine which audience segments exist, run get_all_audience_segments.py.
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

AUDIENCE_SEGMENT_ID = 'INSERT_AUDIENCE_SEGMENT_ID_HERE'


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

# Initialize appropriate service.
audience_segment_service = client.GetService(
    'AudienceSegmentService', version='v201308')

# Specify bind value to filter on First Party Segments
values = (
    [{'key': 'type',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'FIRST_PARTY'
          }
     },
     {'key': 'audience_segment_id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': AUDIENCE_SEGMENT_ID
          }
     }])

# Create a statement to select first party audience segments.
filter_statement = {'query': ('WHERE Type = :type AND Id = '
                              ':audience_segment_id LIMIT 1'),
                    'values': values}

response = audience_segment_service.getAudienceSegmentsByStatement(
    filter_statement)[0]

if 'results' in response:
  audience_segments = response['results']

  for audience_segment in audience_segments:
    print ('Audience segment with id \'%s\' and name \'%s\' will be updated.'
           % (audience_segment['id'], audience_segment['name']))

    audience_segment['membershipExpirationDays'] = '180'

  updated_audience_segments = (
      audience_segment_service.updateAudienceSegments(audience_segments))

  for updated_audience_segment in updated_audience_segments:
    print ('Audience segment with id \'%s\' and name \'%s\' was updated' %
           (updated_audience_segment['id'],
            updated_audience_segment['name']))

else:
  print 'No Results Found'
