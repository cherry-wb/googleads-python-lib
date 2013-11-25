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

"""This code example updates the destination URL of all line item creative
associations (LICA) up to the first 500. To determine which LICAs exist, run
get_all_licas.py."""

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

# Create statement object to get all LICAs.
filter_statement = {'query': 'LIMIT 500'}

# Get LICAs by statement.
response = lica_service.GetLineItemCreativeAssociationsByStatement(
    filter_statement)[0]
licas = []
if 'results' in response:
  licas = response['results']

if licas:
  # Update each local LICA object by changing its destination URL.
  for lica in licas:
    lica['destinationUrl'] = 'http://news.google.com'

  # Update LICAs remotely.
  licas = lica_service.UpdateLineItemCreativeAssociations(licas)

  # Display results.
  if licas:
    for lica in licas:
      print ('LICA with line item id \'%s\', creative id \'%s\', and status '
             '\'%s\' was updated.' % (lica['lineItemId'], lica['creativeId'],
                                      lica['status']))
  else:
    print 'No LICAs were updated.'
else:
  print 'No LICAs found to update.'
