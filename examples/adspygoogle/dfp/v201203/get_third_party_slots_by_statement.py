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

"""This code example gets archived third party slots. The statement retrieves up
 to the maximum page size limit of 500. To create third party slots, run
create_third_party_slot.py."""

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
third_party_slot_service = client.GetService(
    'ThirdPartySlotService', 'https://www.google.com', 'v201203')

# Create a statement to only select archived third party slots.
values = [{
    'key': 'status',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ARCHIVED'
    }
}]
filter_statement = {'query': 'WHERE status = :status LIMIT 500',
                    'values': values}

# Get third party slots by statement.
response = third_party_slot_service.GetThirdPartySlotsByStatement(
    filter_statement)[0]
third_party_slots = []
if 'results' in response:
  third_party_slots = response['results']

# Display results.
for third_party_slot in third_party_slots:
  print 'Third party slot with id \'%s\' was found.' % third_party_slot['id']

print
print 'Number of results found: %s' % len(third_party_slots)

