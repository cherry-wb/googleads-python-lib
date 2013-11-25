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

"""Unit tests to cover GenericDfaService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
import warnings
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle.dfa import DfaErrors
from adspygoogle.dfa import GenericDfaService


class GenericDfaServiceTest(unittest.TestCase):

  """Tests for the adspygoogle.dfa.GenericDfaService module."""

  def testLegacyPasswordDeprecationWarning_legacyAuth(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = GenericDfaService.GenericDfaService(
          {'Username': 'username', 'Password': 'password'},
          {'access': '', 'units': '0', 'xml_log': 'n', 'request_log': 'n',
           'debug': 'n', 'raw_response': 'n', 'compress': 'n', 'app_name': ''},
          {'server': '', 'version': '', 'http_proxy': ''},
          mock.Mock(), mock.Mock(), 'ServiceInterface')

      with mock.patch('adspygoogle.dfa.GenericDfaService.GenericDfaService.'
                      '_CreateMethod'):
        with warnings.catch_warnings(record=True) as captured_warnings:
          service._GenerateToken()
          self.assertEqual(len(captured_warnings), 1)
          warning = captured_warnings[0]
          self.assertTrue(issubclass(warning.category, DeprecationWarning))
          self.assertEqual(str(warning.message),
                           GenericDfaService._DEPRECATION_WARNING)

  def testLegacyPasswordDeprecationWarning_OAuth2(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = GenericDfaService.GenericDfaService(
          {'Username': 'username', 'oauth2credentials': object()},
          {'access': '', 'units': '0', 'xml_log': 'n', 'request_log': 'n',
           'debug': 'n', 'raw_response': 'n', 'compress': 'n', 'app_name': ''},
          {'server': '', 'version': '', 'http_proxy': ''},
          mock.Mock(), mock.Mock(), 'ServiceInterface')

      with mock.patch('adspygoogle.dfa.GenericDfaService.GenericDfaService.'
                      '_CreateMethod'):
        with warnings.catch_warnings(record=True) as captured_warnings:
          service._GenerateToken()
          self.assertEqual(len(captured_warnings), 0)

  def testWrapSoapCall(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = GenericDfaService.GenericDfaService(
          {'Username': 'username', 'oauth2credentials': object()},
          {'access': '', 'units': '0', 'xml_log': 'n', 'request_log': 'n',
           'debug': 'n', 'raw_response': 'n', 'compress': 'n', 'app_name': ''},
          {'server': '', 'version': '', 'http_proxy': ''},
          mock.Mock(), mock.Mock(), 'ServiceInterface')

    fake_function = mock.Mock()
    service._WrapSoapCall(fake_function)()
    self.assertEqual(1, fake_function.call_count)

    fake_function.reset_mock()
    fake_function.side_effect = DfaErrors.DfaApiError({})
    try:
      service._WrapSoapCall(fake_function)()
    except DfaErrors.DfaApiError:
      self.assertEqual(1, fake_function.call_count)
    else:
      self.fail('Error should have been thrown.')

    fake_function.reset_mock()
    error = DfaErrors.DfaAuthenticationError({})
    error.error_code = 4
    error.message = 'Wrong message.'
    fake_function.side_effect = error
    try:
      service._WrapSoapCall(fake_function)()
    except DfaErrors.DfaAuthenticationError:
      self.assertEqual(1, fake_function.call_count)
    else:
      self.fail('Error should have been thrown.')

    fake_function.reset_mock()
    error = DfaErrors.DfaAuthenticationError({})
    error.error_code = 4
    error.message = (
        GenericDfaService.GenericDfaService._TOKEN_EXPIRED_ERROR_MESSAGE)
    soap_call_rvals = [{}, error]
    def ReturnFunction(*unused_args, **unused_kargs):
      rval = soap_call_rvals.pop()
      if isinstance(rval, Exception):
        raise rval
      return rval

    fake_function.side_effect = ReturnFunction
    with mock.patch('adspygoogle.dfa.GenericDfaService.GenericDfaService.'
                    '_GenerateToken') as mock_generate_token:
      service._WrapSoapCall(fake_function)()
      self.assertEqual(2, fake_function.call_count)
      self.assertEqual(1, mock_generate_token.call_count)


if __name__ == '__main__':
  unittest.main()
