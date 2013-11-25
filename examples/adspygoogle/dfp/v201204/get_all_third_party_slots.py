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

"""This example gets all third party slots. To create a third party slot, run
create_third_party_slot.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
third_part_slot_service = client.GetService(
    'ThirdPartySlotService', version='v201204')

# Get third part slots by statement.
third_part_slots = DfpUtils.GetAllEntitiesByStatementWithService(
    third_part_slot_service)

# Display results.
for third_part_slot in third_part_slots:
  print 'Third party slot with id \'%s\' was found.' % third_part_slot['id']

print
print 'Number of results found: %s' % len(third_part_slots)
