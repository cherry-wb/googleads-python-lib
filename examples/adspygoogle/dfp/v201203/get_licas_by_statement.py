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

"""This code example gets all line item creative associations (LICA) for a given
line item id. The statement retrieves up to the maximum page size limit of 500.
To create LICAs, run create_licas.py."""

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
lica_service = client.GetService(
    'LineItemCreativeAssociationService', 'https://www.google.com', 'v201203')

# Set the id of the line item to get LICAs by.
line_item_id = 'INSERT_LINE_ITEM_ID_HERE'

# Create statement object to only select LICAs for the given line item id.
values = [{
    'key': 'lineItemId',
    'value': {
        'xsi_type': 'NumberValue',
        'value': line_item_id
    }
}]
filter_statement = {'query': 'WHERE lineItemId = :lineItemId LIMIT 500',
                    'values': values}

# Get LICAs by statement.
response = lica_service.GetLineItemCreativeAssociationsByStatement(
    filter_statement)[0]
licas = []
if 'results' in response:
  licas = response['results']

# Display results.
for lica in licas:
  print ('LICA with line item id \'%s\', creative id \'%s\', and status '
         '\'%s\' was found.' % (lica['id'], lica['creativeId'], lica['status']))

print
print 'Number of results found: %s' % len(licas)
