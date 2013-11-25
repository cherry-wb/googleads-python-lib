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

"""This example gets existing DFA sites based on a given search criteria.
Results are limited to the first 10.

Tags: site.getDfaSites
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  site_service = client.GetSiteService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Create DFA site search criteria structure.
  dfa_site_search_criteria = {
      'pageSize': '10'
  }

  # Get the sites.
  results = site_service.GetDfaSites(dfa_site_search_criteria)[0]

  # Display DFA site names and IDs.
  if results['records']:
    for dfa_site in results['records']:
      print ('DFA site with name \'%s\' and ID \'%s\' was found.'
             % (dfa_site['name'], dfa_site['id']))
  else:
    print 'No DFA sites found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
