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

"""Test to cover issue 51.

Ensures when using PyXML and pretty_print turned off, the library is able to
deserialize AdWords errors.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock
from oauth2client.client import OAuth2Credentials

from adspygoogle import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsRequestError
from adspygoogle.adwords.AdWordsSoapBuffer import AdWordsSoapBuffer



# Location of a cached buffer to parse.
BUFFER_FILE_LOCATION = os.path.join('..', 'data', 'issue51_buffer.txt')


class Issue51Test(unittest.TestCase):

  """Tests for Issue 51."""

  def testParseError_PyXML_PrettyOff(self):
    """Tests that the SOAP buffer parses AdWords errors correctly."""
    self._RunTestWithBuffer(AdWordsSoapBuffer('1', False))

  def testParseError_PyXML_PrettyOn(self):
    """Tests that the SOAP buffer parses AdWords errors correctly."""
    self._RunTestWithBuffer(AdWordsSoapBuffer('1', True))

  def testParseError_ETree_PrettyOff(self):
    """Tests that the SOAP buffer parses AdWords errors correctly."""
    self._RunTestWithBuffer(AdWordsSoapBuffer('2', False))

  def testParseError_ETree_PrettyOn(self):
    """Tests that the SOAP buffer parses AdWords errors correctly."""
    self._RunTestWithBuffer(AdWordsSoapBuffer('2', True))

  def _RunTestWithBuffer(self, buffer_):
    """Tests error parsing using the given AdWordsSoapBuffer."""
    client = AdWordsClient(headers={
        'userAgent': 'USER_AGENT',
        'developerToken': 'DEVELOPER_TOKEN',
        'clientCustomerId': 'CLIENT_CUSTOMER_ID',
        'oauth2credentials': OAuth2Credentials(
            'ACCESS_TOKEN', 'client_id', 'client_secret', 'refresh_token', None,
            'uri', 'user_agent')
    })

    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = client.GetCampaignService()

    buffer_.write(open(BUFFER_FILE_LOCATION).read())

    try:
      service._HandleLogsAndErrors(buffer_, '', '', {'data': 'datum'})
    except AdWordsRequestError, e:
      self.assertEqual(-1, e.code)
      self.assertEqual(1, len(e.errors))
      error_detail = e.errors[0]
      self.assertEqual('Please correct the capitalization in the following '
                       'phrase(s): \'AAAAAAAAAAAAAAAAAAAAA\'',
                       error_detail.externalPolicyDescription)
      self.assertEqual('[Capitalization] Excessive capitalization',
                       error_detail.externalPolicyName)
      self.assertEqual(None, error_detail.externalPolicyUrl)
      self.assertEqual('true', error_detail.isExemptable)
      self.assertEqual('operations[0].operand.ad.headline',
                       error_detail.fieldPath)
      self.assertEqual('PolicyViolationError', error_detail.type)
      self.assertEqual(None, error_detail.trigger)
      self.assertEqual({'policyName': 'capitalization',
                        'violatingText': 'AAAAAAAAAAAAAAAAAAAAA'},
                       error_detail.key)
      self.assertEqual({'index': '0', 'length': '21'},
                       error_detail.violatingParts)


if __name__ == '__main__':
  unittest.main()
