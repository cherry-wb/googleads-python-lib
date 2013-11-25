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

"""Unit tests to cover GenericAdWordsService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.GenericAdWordsService import GenericAdWordsService


class UtilsTest(unittest.TestCase):

  """Tests for the adspygoogle.adwords.GenericAdWordsService module."""

  def testHandleLogsAndErrors_faultIsAString(self):
    """Tests the _HandleLogsAndErrors function accepts string errors."""
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = GenericAdWordsService(
          {}, {'access': '', 'units': '0', 'xml_log': 'n', 'request_log': 'n',
               'debug': 'n', 'raw_response': 'n'},
          {'group': 'cm', 'server': '', 'version': '', 'http_proxy': ''},
          object(), object(), 'ServiceInterface')

    buffer_ = mock.Mock()
    rvals = {
        'GetFaultAsDict.return_value': 'This is a string error message',
        'GetCallUnits.return_value': 0,
        'GetCallOperations.return_value': 0,
    }
    buffer_.configure_mock(**rvals)

    self.assertRaises(AdWordsError, service._HandleLogsAndErrors,
                      buffer_, '', '', {'data': 'datum'})

  def testHandleLogsAndErrors_faultIsAUnicode(self):
    """Tests the _HandleLogsAndErrors function accepts unicode errors."""
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = GenericAdWordsService(
          {}, {'access': '', 'units': '0', 'xml_log': 'n', 'request_log': 'n',
               'debug': 'n', 'raw_response': 'n'},
          {'group': 'cm', 'server': '', 'version': '', 'http_proxy': ''},
          object(), object(), 'ServiceInterface')

    buffer_ = mock.Mock()
    rvals = {
        'GetFaultAsDict.return_value': u'This is a string error message',
        'GetCallUnits.return_value': 0,
        'GetCallOperations.return_value': 0,
    }
    buffer_.configure_mock(**rvals)

    self.assertRaises(AdWordsError, service._HandleLogsAndErrors,
                      buffer_, '', '', {'data': 'datum'})


if __name__ == '__main__':
  unittest.main()
