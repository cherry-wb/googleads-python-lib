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

"""This code example updates the notes of each order up to the first 500. To
determine which orders exist, run get_all_orders.py."""

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
order_service = client.GetService('OrderService', version='v201204')

# Create statement object to get all orders.
filter_statement = {'query': 'LIMIT 500'}

# Get orders by statement.
response = order_service.GetOrdersByStatement(filter_statement)[0]
orders = []
if 'results' in response:
  orders = response['results']

if orders:
  # Update each local order object by changing its notes.
  updated_orders = []
  for order in orders:
    # Archived orders cannot be updated.
    if not Utils.BoolTypeConvert(order['isArchived']):
      order['notes'] = 'Spoke to advertiser. All is well.'
      updated_orders.append(order)

  # Update orders remotely.
  orders = order_service.UpdateOrders(updated_orders)

  # Display results.
  if orders:
    for order in orders:
      print ('Order with id \'%s\', name \'%s\', advertiser id \'%s\', and '
             'notes \'%s\' was updated.'
             % (order['id'], order['name'], order['advertiserId'],
                order['notes']))
  else:
    print 'No orders were updated.'
else:
  print 'No orders found to update.'
