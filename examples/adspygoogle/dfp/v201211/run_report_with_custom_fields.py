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

"""This code example runs a report that includes custom fields found in the line
items of an order. To download the report run download_report.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import time

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate services.
line_item_service = client.GetService('LineItemService', version='v201211')
report_service = client.GetService('ReportService', version='v201211')

# Set the ID of the order to get line items from.
order_id = 'INSERT_ORDER_ID_HERE'

# Filter for line items of a given order.
values = [{
    'key': 'orderId',
    'value': {
        'xsi_type': 'NumberValue',
        'value': order_id
    }
}]
query = 'WHERE orderId = :orderId'

# Get the line items by statement.
line_items = DfpUtils.GetAllEntitiesByStatementWithService(line_item_service,
                                                           query=query,
                                                           bind_vars=values)

# Collect all line item custom field IDs for an order.
custom_field_ids = []

# Get custom field IDs from the line items of an order.
for line_item in line_items:
  if 'customFieldValues' in line_item:
    for custom_field_value in line_item['customFieldValues']:
      custom_field_id = custom_field_value['customFieldId']
      if custom_field_id not in custom_field_ids:
        custom_field_ids.append(custom_field_id)

# Create statement object to filter for an order.
filter_statement = {'query': 'WHERE ORDER_ID = :orderId',
                    'values': values}

# Create report job.
report_job = {
    'reportQuery': {
        'dimensions': ['LINE_ITEM'],
        'statement': filter_statement,
        'columns': ['AD_SERVER_IMPRESSIONS'],
        'dateRangeType': 'LAST_MONTH',
        'customFieldIds': custom_field_ids
    }
}

# Run report.
report_job = report_service.RunReportJob(report_job)[0]

# Wait for report to complete.
status = report_job['reportJobStatus']
while status != 'COMPLETED' and status != 'FAILED':
  print 'Report job with \'%s\' id is still running.' % report_job['id']
  time.sleep(30)
  status = report_service.GetReportJob(report_job['id'])[0]['reportJobStatus']

if status == 'FAILED':
  print ('Report job with id \'%s\' failed to complete successfully.'
         % report_job['id'])
else:
  print 'Report job with id \'%s\' completed successfully.' % report_job['id']
