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

"""This code example creates a new third party slot. To determine which
companies exist, run get_all_companies.py. To determine which creatives exist,
run get_all_creatives.py"""

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
    'ThirdPartySlotService', version='v201204')

company_id = 'INSERT_COMPANY_ID_HERE'
external_unique_id = 'INSERT_EXTERNAL_UNIQUE_ID_HERE'
external_unique_name = 'INSERT_EXTERNAL_UNIQUE_NAME_HERE'
creative_ids = ['INSERT_CREATIVE_ID_HERE']

# Create a third party slot object.
third_party_slot = {
    'companyId': company_id,
    'description': 'Third party slot description.',
    'externalUniqueId': external_unique_id,
    'externalUniqueName': external_unique_name,
    'creativeIds': creative_ids
}

# Add the third party slot.
third_party_slot = third_party_slot_service.CreateThirdPartySlot(
    third_party_slot)[0]

# Display results.
if third_party_slot:
  print ('A third party slot with id \'%s\' and named \'%s\' was created.'
         % (third_party_slot['id'], third_party_slot['externalUniqueName']))
else:
  print 'No third party slot created.'
