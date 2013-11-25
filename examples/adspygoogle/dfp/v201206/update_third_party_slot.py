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

"""This code example updates the first third party slot's description."""

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
    'ThirdPartySlotService', version='v201206')

# Create statement object to only select third party slots that are active.
values = [{
    'key': 'status',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ACTIVE'
    }
}]
filter_statement = {'query': 'WHERE status = :status LIMIT 1',
                    'values': values}

# Get a third party slot by statement.
response = third_party_slot_service.GetThirdPartySlotsByStatement(
    filter_statement)[0]
third_party_slots = []
if 'results' in response:
  third_party_slots = response['results']

if third_party_slots:
  # Update the local third party slot object by changing the description.
  third_party_slot = third_party_slots[0]
  third_party_slot['description'] = 'Updated description.'

  # Update third party slots remotely.
  third_party_slot = third_party_slot_service.UpdateThirdPartySlot(
      third_party_slot)[0]

  # Display results.
  if third_party_slot:
    print ('A third party slot with id \'%s\' and description \'%s\' was '
           'updated.' % (third_party_slot['id'],
                         third_party_slot['description']))
  else:
    print 'No third party slots were updated.'
else:
  print 'No third party slots found to update.'
