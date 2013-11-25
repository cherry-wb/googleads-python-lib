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

"""This code example gets all line items that need creatives for the given
order. The statement retrieves up to the maximum page size limit of 500. To
create line items, run create_line_items.py."""

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
line_item_service = client.GetService(
    'LineItemService', 'https://www.google.com', 'v201203')

# Set the id of the order to get line items from.
order_id = 'INSERT_ORDER_ID_HERE'

# Create statement object to only select line items that need creatives from a
# given order.
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
filter_statement = {
    'query': 'WHERE orderId = :orderId AND status = :status LIMIT 500',
    'values': values
}

# Get line items by statement.
response = line_item_service.GetLineItemsByStatement(filter_statement)[0]
line_items = []
if 'results' in response:
  line_items = response['results']

# Display results.
for line_item in line_items:
  print ('Line item with id \'%s\', belonging to order id \'%s\', and named '
         '\'%s\' was found.' % (line_item['id'], line_item['orderId'],
                                line_item['name']))

print
print 'Number of results found: %s' % len(line_items)
