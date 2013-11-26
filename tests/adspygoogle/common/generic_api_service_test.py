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

"""Unit tests to cover GenericApiService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import datetime
import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock
from oauth2client.client import OAuth2Credentials

from adspygoogle.common.GenericApiService import GenericApiService
from adspygoogle.common.SoapBuffer import SoapBuffer


class ConcreteGenericApiService(GenericApiService):

  """A subclass of the abstract GenericApiService class, used for testing."""

  def _HandleLogsAndErrors(self, unused_buf, unused_start, unused_stop):
    """Dummy implementation of an abstract method in GenericApiService."""
    pass


class GenericApiServiceTest(unittest.TestCase):

  """Tests for the adspygoogle.common.GenericApiService module."""

  def testCallRawMethod_oauth2(self):
    """Tests the CallRawMethod function with OAuth 2."""
    credentials = OAuth2Credentials(
        'ACCESS_TOKEN', 'client_id', 'client_secret', 'refresh_token', None,
        'uri', 'user_agent')

    headers = {'oauth2credentials': credentials}
    config = {
        'xml_parser': '2',
        'pretty_xml': 'y',
        'wrap_in_tuple': 'y'
    }
    op_config = {
        'http_proxy': None,
        'server': 'www.myurl.com',
    }
    lock = logger = mock.Mock()
    service_name = namespace = ''
    service_url = 'campaigns/and/stuff'
    namespace_extractor = lambda x: x
    buffer_class = SoapBuffer
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = ConcreteGenericApiService(
          headers, config, op_config, lock, logger, service_name, service_url,
          True, buffer_class, namespace, namespace_extractor)

    message = 'Moocow'
    response = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<soapenv:Envelope '
        'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        '<soapenv:Header>\n'
        '</soapenv:Header>\n'
        '<soapenv:Body>\n'
        '<ns2:Response '
        'soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" '
        'xmlns:ns2="http://www.doubleclick.net/dfa-api/v1.19">\n'
        '<email xsi:type="soapenc:string">test@test.com</email>\n'
        '</ns2:Response>\n'
        '</soapenv:Body>\n'
        '</soapenv:Envelope>\n')

    with mock.patch('httplib.HTTPS') as https_:
      mock_https = https_(op_config['server'])
      mock_response = mock.Mock()
      rvals = {
          'getreply.return_value': (200, 'OK', {}),
          'getfile.return_value': mock_response
      }
      mock_https.configure_mock(**rvals)
      response_rvals = {
          'read.return_value': response
      }
      mock_response.configure_mock(**response_rvals)

      output = service.CallRawMethod(message)
      self.assertEqual((response,), output)

      mock_https.putrequest.assert_called_with('POST', service_url)

      expected_http_headers = [
          mock.call('Host', ''),
          mock.call('User-Agent', 'ConcreteGenericApiService; CallRawMethod'),
          mock.call('Content-type', 'text/xml; charset="UTF-8"'),
          mock.call('Content-length', '6'),
          mock.call('SOAPAction', ''),
          mock.call('Authorization', 'Bearer ACCESS_TOKEN')
      ]
      mock_https.putheader.assert_has_calls(expected_http_headers)

      mock_https.endheaders.assert_called_once_with()
      mock_https.send.assert_called_once_with(message)

  def testReadyOAuth_usingOAuth_refresh(self):
    credentials = mock.Mock()
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = ConcreteGenericApiService(
          {'oauth2credentials': credentials},
          {'xml_parser': '2', 'pretty_xml': 'y', 'wrap_in_tuple': 'y'},
          {'http_proxy': None, 'server': 'www.myurl.com'}, mock.Mock(),
          mock.Mock(), '', '', True, '', '', '')

    rvals = {
        'token_expiry': datetime.datetime(1980, 1, 1, 12)
    }
    credentials.configure_mock(**rvals)

    service._ReadyOAuth()

    credentials.refresh.assert_called_once_with(mock.ANY)
    credentials.apply.assert_called_once_with(mock.ANY)

  def testReadyOAuth_usingOAuth_noRefresh(self):
    credentials = mock.Mock()
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = ConcreteGenericApiService(
          {'oauth2credentials': credentials},
          {'xml_parser': '2', 'pretty_xml': 'y', 'wrap_in_tuple': 'y'},
          {'http_proxy': None, 'server': 'www.myurl.com'}, mock.Mock(),
          mock.Mock(), '', '', True, '', '', '')

    rvals = {
        'token_expiry': datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    }
    credentials.configure_mock(**rvals)

    service._ReadyOAuth()

    self.assertFalse(credentials.refresh.called)
    credentials.apply.assert_called_once_with(mock.ANY)

  def testRefreshCredentialIfNecessary_refresh(self):
    credentials = mock.Mock()
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = ConcreteGenericApiService(
          {'oauth2credentials': credentials},
          {'xml_parser': '2', 'pretty_xml': 'y', 'wrap_in_tuple': 'y'},
          {'http_proxy': None, 'server': 'www.myurl.com'}, mock.Mock(),
          mock.Mock(), '', '', True, '', '', '')

    rvals = {
        'token_expiry': datetime.datetime(1980, 1, 1, 12)
    }
    credentials.configure_mock(**rvals)

    service._RefreshCredentialIfNecessary(credentials)

    credentials.refresh.assert_called_once_with(mock.ANY)

  def testRefreshCredentialIfNecessary_noRefresh(self):
    credentials = mock.Mock()
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = ConcreteGenericApiService(
          {'oauth2credentials': credentials},
          {'xml_parser': '2', 'pretty_xml': 'y', 'wrap_in_tuple': 'y'},
          {'http_proxy': None, 'server': 'www.myurl.com'}, mock.Mock(),
          mock.Mock(), '', '', True, '', '', '')

    rvals = {
        'token_expiry': datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    }
    credentials.configure_mock(**rvals)

    service._RefreshCredentialIfNecessary(credentials)

    self.assertFalse(credentials.refresh.called)


if __name__ == '__main__':
  unittest.main()
