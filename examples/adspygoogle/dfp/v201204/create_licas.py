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

"""This code example creates new line item creative associations (LICAs) for an
existing line item and a set of creative ids. For small business networks,
the creative ids must represent new or copied creatives as creatives cannot be
used for more than one line item. For premium solution networks, the reative ids
can represent any creatvie. To copy creatives, run copy_image_creatives.py. To
determine which LICAs exist, run get_all_licas.py."""

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
    'LineItemCreativeAssociationService', version='v201204')
creative_service = client.GetService('CreativeService', version='v201204')

# Set the line item ID and creative IDs to associate.
line_item_id = 'INSERT_LINE_ITEM_ID_HERE'
order_id = 'INSERT_ORDER_ID_HERE'
creative_ids = ['INSERT_CREATIVE_ID_HERE']

licas = []
for creative_id in creative_ids:
  licas.append({'creativeId': creative_id,
                'lineItemId': line_item_id})

# Create the LICAs remotely.
licas = lica_service.CreateLineItemCreativeAssociations(licas)

# Display results.
if licas:
  for lica in licas:
    print ('LICA with line item id \'%s\', creative id \'%s\', and '
           'status \'%s\' was created.' % (lica['id'], lica['creativeId'],
                                           lica['status']))
else:
  print 'No LICAs created.'
