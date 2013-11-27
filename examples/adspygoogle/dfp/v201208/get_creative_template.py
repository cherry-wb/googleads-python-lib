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

"""This code example gets a creative template by its id."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
creative_template_service = client.GetService(
    'CreativeTemplateService', version='v201208')

# Set id of the creative to get.
creative_template_id = 'CREATIVE_TEMPLATE_ID_HERE'

# Get creative.
template = creative_template_service.getCreativeTemplate(
    creative_template_id)[0]

# Display results.
print ('Creative template with id \'%s\', name \'%s\', and type \'%s\' was '
       'found.') % (template['id'], template['name'], template['type'])

for variable in template['variables']:
  if Utils.BoolTypeConvert(variable['isRequired']):
    print 'Variable with name \'%s\' is required.' % variable['uniqueName']
  else:
    print 'Variable with name \'%s\' is optional.' % variable['uniqueName']
