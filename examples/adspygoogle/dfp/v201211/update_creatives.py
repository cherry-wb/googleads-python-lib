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

"""This code example updates the destination URL of all image creatives up to
the first 500. To determine which image creatives exist, run
get_all_creatives.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
creative_service = client.GetService('CreativeService', version='v201211')

# Create statement object to get all image creatives.
values = [{
    'key': 'type',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ImageCreative'
    }
}]
filter_statement = {'query': 'WHERE creativeType = :type LIMIT 500',
                    'values': values}

# Get creatives by statement.
response = creative_service.GetCreativesByStatement(filter_statement)[0]
creatives = []
if 'results' in response:
  creatives = response['results']

if creatives:
  # Update each local creative object by changing its destination URL.
  for creative in creatives:
    creative['destinationUrl'] = 'http://news.google.com'

  # Update creatives remotely.
  creatives = creative_service.UpdateCreatives(creatives)

  # Display results.
  if creatives:
    for creative in creatives:
      print ('Image creative with id \'%s\' and destination URL \'%s\' was '
             'updated.' % (creative['id'], creative['destinationUrl']))
  else:
    print 'No orders were updated.'
else:
  print 'No orders found to update.'
