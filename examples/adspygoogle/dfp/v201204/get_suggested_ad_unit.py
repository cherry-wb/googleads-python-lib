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

"""This code example gets a suggested ad unit by its id. To determine which
suggested ad units exist, run get_all_suggested_ad_units.py. This feature is
only available to DFP premium solution networks."""

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
suggested_ad_unit_service = client.GetService(
    'SuggestedAdUnitService', version='v201204')

# Set the id of the suggested ad unit to get.
suggested_ad_unit_id = 'INSERT_SUGGESTED_AD_UNIT_ID_HERE'

# Get suggested ad unit.
suggested_ad_unit = suggested_ad_unit_service.GetSuggestedAdUnit(
    suggested_ad_unit_id)[0]

# Display results.
print ('Suggested ad unit with id \'%s\' and number of requests \'%s\' was '
       'found.') % (suggested_ad_unit['id'], suggested_ad_unit['numRequests'])
