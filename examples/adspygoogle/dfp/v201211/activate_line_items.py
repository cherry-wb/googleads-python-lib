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

"""This code example activates all line items for the given order. To be
activated, line items need to be in the approved state and have at least one
creative associated with them. To approve line items, approve the order to
which they belong by running approve_orders.py. To create LICAs, run
create_licas.py. To determine which line items exist, run
get_all_line_items.py."""

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
line_item_service = client.GetService('LineItemService', version='v201211')

# Set the id of the order to get line items from.
order_id = 'INSERT_ORDER_ID_HERE'

# Create query.
values = [{
    'key': 'orderId',
    'value': {
        'xsi_type': 'NumberValue',
        'value': order_id
    }
}, {
    'key': 'status',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'NEEDS_CREATIVES'
    }
}]
query = 'WHERE orderId = :orderId AND status = :status'

# Get line items by statement.
line_items = DfpUtils.GetAllEntitiesByStatementWithService(
    line_item_service, query=query, bind_vars=values)
for line_item in line_items:
  print ('Line item with id \'%s\', belonging to order id \'%s\', and name '
         '\'%s\' will be activated.' % (line_item['id'], line_item['orderId'],
                                        line_item['name']))
print 'Number of line items to be activated: %s' % len(line_items)

# Perform action.
result = line_item_service.PerformLineItemAction(
    {'type': 'ActivateLineItems'}, {'query': query, 'values': values})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of line items activated: %s' % result['numChanges']
else:
  print 'No line items were activated.'
