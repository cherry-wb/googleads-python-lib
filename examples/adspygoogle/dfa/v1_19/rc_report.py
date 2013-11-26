#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""This example mimics the RCRunner file "RCReport" but uses the DFA API instead
of the Java DART API. It shows how to request the generation of a deferred
report, how to check to see when it is done, and how to download it when it is
completed.

Tags: report.getReport, report.runDeferredReport
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import time
import urllib

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


if len(sys.argv) != 5:
  print ('This program requires 4 command line arguments:\n'
         '\t1. DFA username\n\t2. DFA password\n'
         '\t3. Query ID number\n\t4. Output filename.\n')
  print ('Example usage: python rc_report.py username@dfa password456 12345 '
         'report.zip')
  sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
query_id = sys.argv[3]
output_file_name = sys.argv[4]

# Initialize client object.
client = DfaClient()
client._headers['Username'] = username
client._headers['Password'] = password

# Initialize appropriate service.
report_service = client.GetReportService(
    'http://advertisersapitest.doubleclick.net', 'v1.19')

# Create report request and submit it to the server.
report_request = {
    'queryId': query_id,
}
report_info = report_service.RunDeferredReport(report_request)[0]
print 'Report with ID \'%s\' has been scheduled.' % (report_info['reportId'])

report_request['reportId'] = report_info['reportId']

while(not report_info['status']['name'] == 'COMPLETE'):
  print ('Still waiting for report with ID \'%s\', current status is \'%s\'.'
         % (report_info['reportId'], report_info['status']['name']))
  print 'Waiting 10 minutes before checking on report status.'
  time.sleep(600)
  report_info = report_service.GetReport(report_request)[0];
  if report_info['status']['name'] == 'ERROR':
    print 'Deferred report failed with errors. Run in the UI to troubleshoot.'
    sys.exit(1)

file = open(output_file_name, 'w')
file.write(urllib.urlopen(report_info['url']).read())

print 'Report downloaded to %s.' % output_file_name
