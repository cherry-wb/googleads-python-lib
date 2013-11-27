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

"""This example requests the generation of a report. Once the report has been
requested, you can continually get updates on the status of the report until it
is completed. There is currently no way to get a query ID through the DFA API;
you must use the website interface or the Java DART API instead. To request an
update on a report's status, run get_report.py.

Tags: report.runDeferredReport
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


QUERY_ID = 'INSERT_QUERY_ID_HERE'


def main(client, query_id):
  # Initialize appropriate service.
  report_service = client.GetReportService(
      'http://advertisersapitest.doubleclick.net', 'v1.19')

  # Create report search criteria structure.
  report_request = {
      'queryId': query_id
  }

  # Request generation of a report for your query.
  report_info = report_service.RunDeferredReport(report_request)[0]

  # Display success message.
  print 'Report with ID \'%s\' has been scheduled.' % (report_info['reportId'])


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, QUERY_ID)
