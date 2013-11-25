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

"""This code example gets up to 500 system defined creative templates."""

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
creative_template_service = client.GetService(
    'CreativeTemplateService', 'https://www.google.com', 'v201203')

# Create statement object to only select system defined creative templates.
values = [{
    'key': 'creativeTemplateType',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'SYSTEM_DEFINED'
    }
}]
filter_statement = {
    'query': 'WHERE type = :creativeTemplateType LIMIT 500',
    'values': values
}

# Get creative templates by statement.
response = creative_template_service.getCreativeTemplatesByStatement(
    filter_statement)[0]
creative_templates = []
if 'results' in response:
  creative_templates = response['results']

# Display results.
for template in creative_templates:
  print ('Creative template with id \'%s\', name \'%s\', and type \'%s\' was '
         'found.') % (template['id'], template['name'], template['type'])

print
print 'Number of results found: %s' % len(creative_templates)
