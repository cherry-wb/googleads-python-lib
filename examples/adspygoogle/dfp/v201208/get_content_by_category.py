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

"""This code example gets all active content categorized as a "comedy" using the
network's content browse custom targeting key. This feature is only available to
DFP video publishers."""

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
content_service = client.GetService('ContentService', version='v201208')

network_service = client.GetService('NetworkService', version='v201208')

custom_targeting_service = client.GetService(
    'CustomTargetingService', version='v201208')

# Get the network's content browse custom targeting key.
network = network_service.GetCurrentNetwork()[0]
key_id = network['contentBrowseCustomTargetingKeyId']

# Create a statement to select the categories matching the name comedy.
values = [
    {
        'key': 'contentBrowseCustomTargetingKeyId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': key_id
        }
    },
    {
        'key': 'category',
        'value': {
            'xsi_type': 'TextValue',
            'value': 'comedy'
        }
    }
]

category_filter_statement = {
    'query': ('WHERE customTargetingKeyId = :contentBrowseCustomTargetingKeyId '
              'and name = :category LIMIT 1'),
    'values': values
}

# Get categories matching the filter statement.
response = custom_targeting_service.GetCustomTargetingValuesByStatement(
    category_filter_statement)[0]

# Get the custom targeting value ID for the comedy category.
category_custom_targeting_value_id = ''
if 'results' in response:
  category_custom_targeting_value_id = response['results'][0]['id']

all_content = []
offset = 0

while True:
  # Create a filter statement to get content.
  filter_statement = {
      'query': 'WHERE status = \'ACTIVE\' LIMIT 500 OFFSET %s' % offset
  }

  # Get the content by statement and custom targeting value.
  response = content_service.GetContentByStatementAndCustomTargetingValue(
      filter_statement, category_custom_targeting_value_id)[0]

  if 'results' in response:
    all_content.extend(response['results'])
    offset += 500
  else:
    break

# Display results.
for content_item in all_content:
  print ('Content with id \'%s\', name \'%s\', and status \'%s\' was found.'
         % (content_item['id'], content_item['name'], content_item['status']))

print
print 'Number of results found: %s' % len(all_content)

