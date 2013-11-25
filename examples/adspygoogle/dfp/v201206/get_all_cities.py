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

"""This example gets all cities available to target.
A full list of available tables can be found at
https://developers.google.com/doubleclick-publishers/docs/reference/v201206/PublisherQueryLanguageService
"""

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
pql_service = client.GetService(
    'PublisherQueryLanguageService', version='v201206')

# Create statement to select all targetable cities.
# A limit of 500 is set here. You may want to page through such a large
# result set.
# For criteria that do not have a "targetable" property, that predicate
# may be left off, i.e. just "SELECT * FROM Browser_Groups LIMIT 500"
select_statement = {'query':
                    'SELECT * FROM City WHERE targetable = true LIMIT 500'}

# Get cities by statement.
result_set = pql_service.Select(select_statement)[0]

# Display results.
if result_set:
  column_labels = [label['labelName'] for label in result_set['columnTypes']]
  print 'Columns are: %s' % ', '.join(column_labels)
  for row in result_set['rows']:
    values = [value.get('value', '') for value in row['values']]
    print 'Values are: %s' % ', '.join(values).encode('utf-8')
else:
  print 'No results found.'
