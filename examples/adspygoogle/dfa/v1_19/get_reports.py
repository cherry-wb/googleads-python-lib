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

"""This example fetches information about all reports generated from the same
query, including their status (pending, running, complete, etc.) and URLs
where they can be downloaded if completed. There is currently no way to get a
query ID through the DFA API; you must use the website interface or the Java
DART API instead.

Tags: report.getReportsByCriteria
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


QUERY_ID = 'INSERT_QUERY_ID_HERE'


def main(client, query_id):
  # Initialize appropriate service.
  report_service = client.GetReportService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Create report search criteria structure.
  report_search_criteria = {
      'queryId': query_id
  }

  # Fetch report information.
  results = report_service.GetReportsByCriteria(report_search_criteria)[0]

  # Display information on reports.
  if results['records']:
    for report_info in results['records']:
      print ('Report with ID \'%s\', status of \'%s\', and URL of \'%s\' was'
             ' found.' % (report_info['reportId'],
                          report_info['status']['name'], report_info['url']))
  else:
    print 'No reports found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, QUERY_ID)
