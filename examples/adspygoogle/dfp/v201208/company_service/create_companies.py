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

"""This code example creates new companies.

To determine which companies exist, run get_all_companies.py.

Tags: CompanyService.createCompanies
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


def main(client):
  # Initialize appropriate service.
  company_service = client.GetService('CompanyService', version='v201208')

  # Create company objects.
  companies = [
      {
          'name': 'Advertiser #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      },
      {
          'name': 'Agency #%s' % Utils.GetUniqueName(),
          'type': 'AGENCY'
      }
  ]

  # Add companies.
  companies = company_service.CreateCompanies(companies)

  # Display results.
  for company in companies:
    print ('Company with ID \'%s\', name \'%s\', and type \'%s\' was created.'
           % (company['id'], company['name'], company['type']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
