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

"""This code example approves all eligible draft and pending orders. To
determine which orders exist, run get_all_orders.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import datetime
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
order_service = client.GetService('OrderService', version='v201211')

# Create query.
values = [{
    'key': 'today',
    'value': {
        'xsi_type': 'TextValue',
        'value': datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S')
    }
}]
query = ('WHERE status in (\'DRAFT\', \'PENDING_APPROVAL\')'
         ' AND endDateTime >= :today AND isArchived = FALSE')

# Get orders by statement.
orders = DfpUtils.GetAllEntitiesByStatementWithService(
    order_service, query=query, bind_vars=values)
for order in orders:
  print ('Order with id \'%s\', name \'%s\', and status \'%s\' will be '
         'approved.' % (order['id'], order['name'], order['status']))
print 'Number of orders to be approved: %s' % len(orders)

# Perform action.
result = order_service.PerformOrderAction({'type': 'ApproveOrders'},
                                          {'query': query, 'values': values})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of orders approved: %s' % result['numChanges']
else:
  print 'No orders were approved.'
