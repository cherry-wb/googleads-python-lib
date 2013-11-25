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

"""Test to cover a regression from the fix to issue 51.

Ensures when pretty_xml is turned off, the library is able to deserialize DFA
errors.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle import DfaClient
from adspygoogle.dfa.DfaErrors import DfaApiError
from adspygoogle.dfa.DfaSoapBuffer import DfaSoapBuffer



# Location of a cached buffer to parse.
BUFFER_FILE_LOCATION = os.path.join('..', 'data', 'issue51_buffer.txt')


class Issue51Test(unittest.TestCase):
  """Tests for Issue 51."""

  def _RunTestWithBuffer(self, buffer_):
    """Tests error parsing using the given DfaSoapBuffer."""
    client = DfaClient(headers={
        'Username': 'username',
        'Password': 'secret',
        'AuthToken': 'password'
    })

    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = client.GetSpotlightService()

    buffer_ = DfaSoapBuffer('1', True)
    buffer_.write(open(BUFFER_FILE_LOCATION).read())

    try:
      service._HandleLogsAndErrors(buffer_, '', '', {'data': 'datum'})
    except DfaApiError, e:
      self.assertEqual('That Activity Group Name or Tag String already exists.',
                       e.error_message)
      self.assertEqual(8304, e.code)
      self.assertEqual('Code 8304: That Activity Group Name or Tag String '
                       'already exists.', str(e))

  def testParseError_PyXML_PrettyOn(self):
    """Tests that the SOAP buffer parses DFA errors correctly."""
    self._RunTestWithBuffer(DfaSoapBuffer('1', True))

  def testParseError_PyXML_PrettyOff(self):
    """Tests that the SOAP buffer parses DFA errors correctly."""
    self._RunTestWithBuffer(DfaSoapBuffer('1', False))

  def testParseError_ETree_PrettyOn(self):
    """Tests that the SOAP buffer parses DFA errors correctly."""
    self._RunTestWithBuffer(DfaSoapBuffer('2', True))

  def testParseError_ETree_PrettyOff(self):
    """Tests that the SOAP buffer parses DFA errors correctly."""
    self._RunTestWithBuffer(DfaSoapBuffer('2', False))


if __name__ == '__main__':
  unittest.main()
