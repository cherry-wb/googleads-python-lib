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

"""This code example updates company comments.

To determine which companies exist, run get_all_companies.py.

Tags: CompanyService.updateCompanies
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

# Set the ID of the company to get.
COMPANY_ID = 'INSERT_COMPANY_ID_HERE'


def main(client, company_id):
  # Initialize appropriate service.
  company_service = client.GetService('CompanyService', version='v201206')

  # Get company.
  company = company_service.GetCompany(company_id)[0]

  if company:
    company['comment'] += ' Updated.'

    # Update the companies on the server.
    companies = company_service.UpdateCompanies([company])

    # Display results.
    if companies:
      for company in companies:
        print (('Company with ID \'%s\', name \'%s\', and comment \'%s\''
                'was updated.')
               % (company['id'], company['name'], company['comment']))
    else:
      print 'No companies were updated.'
  else:
    print 'No companies found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, COMPANY_ID)
