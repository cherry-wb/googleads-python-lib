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

"""Integration test for the AdWords API library using cached OAuth2 values."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Values used for the user agent, developer token, client customer ID, and
# OAuth2 credentials in our test code.
USER_AGENT = 'oauth2_from_file_integration_test'
DEVELOPER_TOKEN = 'INSERT_DEVELOPER_TOKEN_HERE'
CLIENT_CUSTOMER_ID = 'INSERT_CLIENT_CUSTOMER_ID_HERE'
CLIENT_ID = 'INSERT_CLIENT_ID_HERE'
CLIENT_SECRET = 'INSERT_CLIENT_SECRET_HERE'
REFRESH_TOKEN = 'INSERT_REFRESH_TOKEN_HERE'


class AdWordsIntegrationTest(unittest.TestCase):

  """Tests end-to-end usage of the AdWords library."""

  def testRequestWithOAuth2FromFile(self):
    """Tests making a request against AdWords using cached OAuth2 values."""
    path = tempfile.mkdtemp()
    auth_credentials = {
        'clientCustomerId': CLIENT_CUSTOMER_ID,
        'developerToken': DEVELOPER_TOKEN,
        'userAgent': USER_AGENT,
        'clientId': CLIENT_ID,
        'clientSecret': CLIENT_SECRET,
        'refreshToken': REFRESH_TOKEN
    }
    with open(os.path.join(path, 'adwords_api_auth.pkl'), 'w') as handle:
      pickle.dump(auth_credentials, handle)
      handle.close()

    with open(os.path.join(path, 'adwords_api_config.pkl'), 'w') as handle:
      pickle.dump({}, handle)
      handle.close()

    budget = {
        'name': 'Interplanetary budget #%s' % Utils.GetUniqueName(),
        'amount': {
            'microAmount': '50000000'
        },
        'deliveryMethod': 'STANDARD',
        'period': 'DAILY'
    }

    budget_operations = [{
        'operator': 'ADD',
        'operand': budget
    }]

    client = AdWordsClient(path=path)
    budget_service = client.GetBudgetService()
    response = budget_service.Mutate(budget_operations)[0]
    self.assertEqual('BudgetReturnValue', response.get('ListReturnValue_Type'))
    self.assertEqual(1, len(response.get('value', [])))


if __name__ == '__main__':
  unittest.main()
