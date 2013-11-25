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

"""This code example gets all image creatives. The statement retrieves up to the
maximum page size limit of 500. To create an image creative,
run create_creatives.py."""

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
creative_service = client.GetService('CreativeService', version='v201204')

# Create statement object to only select image creatives.
values = [{
    'key': 'creativeType',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ImageCreative'
    }
}]
filter_statement = {'query': 'WHERE creativeType = :creativeType LIMIT 500',
                    'values': values}

# Get creatives by statement.
response = creative_service.GetCreativesByStatement(filter_statement)[0]
creatives = []
if 'results' in response:
  creatives = response['results']

# Display results.
for creative in creatives:
  print ('Creative with id \'%s\', name \'%s\', and type \'%s\' was found.'
         % (creative['id'], creative['name'], creative['Creative_Type']))

print
print 'Number of results found: %s' % len(creatives)
