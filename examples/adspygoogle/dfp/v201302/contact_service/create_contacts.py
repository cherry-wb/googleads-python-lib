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

"""This code example creates new contacts.

To determine which contacts exist, run get_all_contacts.py.

Tags: ContactService.createContacts
"""

__author__ = 'Vincent Tsao'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils

# Set the ID of the advertiser company this contact is associated with.
ADVERTISER_COMPANY_ID = 'INSERT_ADVERTISER_COMPANY_ID_HERE'

# Set the ID of the agency company this contact is associated with.
AGENCY_COMPANY_ID = 'INSERT_AGENCY_COMPANY_ID_HERE'


def main(client, advertiser_company_id, agency_company_id):
  # Initialize appropriate service.
  contact_service = client.GetService('ContactService', version='v201302')

  # Create an advertiser contact.
  advertiser_contact = {
      'name': 'Mr. Advertiser #%s' % Utils.GetUniqueName(),
      'email': 'advertiser@advertising.com',
      'companyId': advertiser_company_id
  }

  # Create an agency contact.
  agency_contact = {
      'name': 'Ms. Agency #%s' % Utils.GetUniqueName(),
      'email': 'agency@agencies.com',
      'companyId': agency_company_id
  }

  # Create the contacts on the server.
  contacts = contact_service.CreateContacts([advertiser_contact,
                                             agency_contact])

  # Display results.
  for contact in contacts:
    print ('Contact with ID \'%s\' name \'%s\' was created.'
           % (contact['id'], contact['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, ADVERTISER_COMPANY_ID, AGENCY_COMPANY_ID)
