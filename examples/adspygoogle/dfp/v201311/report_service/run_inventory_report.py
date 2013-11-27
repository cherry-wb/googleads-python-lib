#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""This code example runs a report equal to the "Whole network report" on the
DFP website. To download the report run download_report.py."""

__author__ = ('Jeff Sham',
              'Vincent Tsao')

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
import time

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

# Initialize appropriate services.
report_service = client.GetService('ReportService', version='v201311')
network_service = client.GetService('NetworkService', version='v201311')

# Get root ad unit id for network.
root_ad_unit_id = (
    network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId'])

# Set filter statement and bind value for reportQuery.
values = [{
    'key': 'ancestor_ad_unit_id',
    'value': {
        'xsi_type': 'NumberValue',
        'value': root_ad_unit_id
    }
}]
filter_statement = {'query': 'WHERE AD_UNIT_ANCESTOR_AD_UNIT_ID'
                             ' = :ancestor_ad_unit_id',
                    'values': values}

# Create report job.
report_job = {
    'reportQuery': {
        'dimensions': ['DATE', 'AD_UNIT_NAME'],
        'adUnitView': 'HIERARCHICAL',
        'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                    'DYNAMIC_ALLOCATION_INVENTORY_LEVEL_IMPRESSIONS',
                    'DYNAMIC_ALLOCATION_INVENTORY_LEVEL_CLICKS',
                    'TOTAL_INVENTORY_LEVEL_IMPRESSIONS',
                    'TOTAL_INVENTORY_LEVEL_CPM_AND_CPC_REVENUE'],
        'dateRangeType': 'LAST_WEEK',
        'statement': filter_statement
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
