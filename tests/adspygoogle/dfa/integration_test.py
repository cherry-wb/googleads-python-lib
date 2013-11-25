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

"""Integration test for end-to-end usage of the DFA API."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle
import shutil
import StringIO
import sys
import tempfile
import unittest
from xml.etree import ElementTree
sys.path.insert(0, os.path.join('..', '..', '..'))


from adspygoogle.dfa import DEFAULT_API_VERSION
from adspygoogle.dfa import LIB_SIG
from adspygoogle.dfa.DfaClient import DfaClient
import mock
from oauth2client.client import OAuth2Credentials



# Location of a cached WSDL to generate a service proxy from.
WSDL_FILE_LOCATION = os.path.join('data', 'placement_service.wsdl')
# Location of a cached login WSDL to generate a service proxy from.
LOGIN_WSDL_FILE_LOCATION = os.path.join('data', 'login_service.wsdl')
# Location of the cached expected SOAP request XML, with some Python string
# formatting operations inside for better flexibility.
REQUEST_FILE_LOCATION = os.path.join('data', 'integration_test_request.xml')

AUTH_REQUEST_FILE_LOCATION = os.path.join('data', 'integration_test_auth_request.xml')
# Location of the cached expected SOAP response XML.
RESPONSE_FILE_LOCATION = os.path.join('data', 'integration_test_response.xml')
# Location of the cached expected authentricate SOAP response XML.
AUTH_RESPONSE_FILE_LOCATION = os.path.join('data', 'integration_test_auth_response.xml')
# Location of the cached expected token expired SOAP response XML.
EXPIRED_RESPONSE_FILE_LOCATION = os.path.join('data', 'integration_test_expired_response.xml')
# Deserialized value of the result stored in the cached SOAP response.
EXPECTED_RESULT = (
    {'name': 'Publisher Paid Regular', 'id': '1'},
    {'name': 'Publisher Paid Interstitial', 'id': '2'},
    {'name': 'Agency Paid Regular', 'id': '3'},
    {'name': 'Agency Paid Interstitial', 'id': '4'},
    {'name': 'Mobile Display', 'id': '7'},
    {'name': 'In-Stream Video', 'id': '6'},
    {'name': 'Publisher Paid In-Stream', 'id': '8'}
)

# Values used in our test code.
ACCESS_TOKEN = 'a1b2c3d4e5'
CLIENT_ID = 'id1234id'
CLIENT_SECRET = 'shhh,itsasecret'
REFRESH_TOKEN = '1/not_a_refresh_token'
OAUTH_URI = 'uri'
USER_AGENT = 'Integration Test'
USER_NAME = 'dfa_user'
TOKEN = 'dfa_token'
EXPIRED_TOKEN = 'expired_token'


class DfaIntegrationTest(unittest.TestCase):

  """Tests end-to-end usage of the DFA library."""

  def testWithPassedInCredential(self):
    """Tests the entire workflow of making a request against DFA.

    Uses a credential passed in to the constructor. Starts with no DFA token and
    has the library generate one.

    Since this library is tightly integrated with SOAPpy, this test mocks out
    the HTTP level rather than the SOAPpy proxy level.
    """
    oauth2_credential = OAuth2Credentials(
        ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, None,
        OAUTH_URI, USER_AGENT)

    headers = {
        'userAgent': USER_AGENT,
        'Username': USER_NAME,
        'oauth2credentials': oauth2_credential
    }
    config = {
        'app_name': USER_AGENT,
        'compress': False
    }
    client = DfaClient(headers=headers, config=config)

    placement_service = self._CreatePlacementService(client)

    page = self._MakeSoapRequest_NoDfaToken(placement_service)
    self.assertEquals(EXPECTED_RESULT, page)

  def testWithCachedRefreshToken(self):
    """Tests the entire workflow of making a request against DFA.

    Uses a cached refresh token to generate a credential. Starts with no DFA
    token and has the library generate one.

    Since this library is tightly integrated with SOAPpy, this test mocks out
    the HTTP level rather than the SOAPpy proxy level.
    """
    directory = self._CreateConfigPickles()

    try:
      with mock.patch(
          'oauth2client.client.OAuth2Credentials.refresh') as mock_refresh:
        client = DfaClient(path=directory)

        self.assertEquals(CLIENT_ID, client.oauth2credentials.client_id)
        self.assertEquals(CLIENT_SECRET, client.oauth2credentials.client_secret)
        self.assertEquals(REFRESH_TOKEN, client.oauth2credentials.refresh_token)

        def SetAccessToken(unused_http):
          client.oauth2credentials.access_token = ACCESS_TOKEN
        mock_refresh.side_effect = SetAccessToken

        placement_service = self._CreatePlacementService(client)

        page = self._MakeSoapRequest_NoDfaToken(placement_service)
        self.assertEquals(EXPECTED_RESULT, page)
        client.oauth2credentials.refresh.assert_called_once_with(mock.ANY)
    finally:
      shutil.rmtree(directory)

  def testExpiredDfaToken(self):
    """Tests regenerating the DFA token once it has expired.

    Uses a credential passed in to the constructor. Starts with an expired DFA
    token and has the library regenerate it.

    Since this library is tightly integrated with SOAPpy, this test mocks out
    the HTTP level rather than the SOAPpy proxy level.
    """
    oauth2_credential = OAuth2Credentials(
        ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, None,
        OAUTH_URI, USER_AGENT)

    headers = {
        'userAgent': USER_AGENT,
        'Username': USER_NAME,
        'oauth2credentials': oauth2_credential,
        'AuthToken': EXPIRED_TOKEN
    }
    config = {
        'app_name': USER_AGENT,
        'compress': False
    }
    client = DfaClient(headers=headers, config=config)

    placement_service = self._CreatePlacementService(client)
    placement_service._config['compress'] = False

    page = self._MakeSoapRequest_ExpiredToken(placement_service)

    self.assertEquals(EXPECTED_RESULT, page)

  def _CreateConfigPickles(self):
    """Creates configuration pickles for testing use of cached values.

    Returns:
      string The directory the pickles were stored in.
    """
    directory = tempfile.mkdtemp()
    auth_credentials = {
        'clientId': CLIENT_ID,
        'clientSecret': CLIENT_SECRET,
        'refreshToken': REFRESH_TOKEN,
        'Username': USER_NAME,
    }
    config = {
        'compress': False,
        'app_name': USER_AGENT
    }
    with open(os.path.join(directory, DfaClient.auth_pkl_name),
              'w') as handle:
      pickle.dump(auth_credentials, handle)

    with open(os.path.join(directory, DfaClient.config_pkl_name),
              'w') as handle:
      pickle.dump(config, handle)

    return directory

  def _CreatePlacementService(self, client):
    """Creates a SOAP service proxy for the DFA placement service.

    All of the network interactions are mocked out.

    Args:
      client: adspygoogle.adwords.DfaClient.DfaClient A client ready to make
              requests against the DFA API.

    Returns:
      adspygoogle.adwords.GenericDfaService.GenericDfaService A service proxy
      for the placement service.
    """
    wsdl_data = open(WSDL_FILE_LOCATION).read() % {'version': DEFAULT_API_VERSION}
    with mock.patch('urllib.urlopen') as mock_urlopen:
      mock_urlopen.return_value = StringIO.StringIO(wsdl_data)
      return client.GetPlacementService()

  def _MakeSoapRequest_NoDfaToken(self, placement_service):
    """Makes a "getPlacementTypes" request against the DFA placement service.

    All of the network interactions are mocked out. This method also makes an
    "authenticate" call against the DFA API.

    Args:
      placement_service: adspygoogle.adwords.GenericDfaService.GenericDfaService
          A service proxy for the DFA placement service.

    Returns:
      tuple The result set from the getPlacementTypes operation.
    """
    request_values = {
        'appName': USER_AGENT,
        'username': USER_NAME,
        'token': TOKEN,
        'libSig': LIB_SIG,
        'version': DEFAULT_API_VERSION
    }
    expected_request = self._GetSoapXml(REQUEST_FILE_LOCATION, request_values)
    expected_auth_request = self._GetSoapXml(AUTH_REQUEST_FILE_LOCATION,
                                             request_values)

    response_values = {
        'version': DEFAULT_API_VERSION,
        'token': TOKEN
    }
    response_xml = self._GetSoapXml(RESPONSE_FILE_LOCATION, response_values)
    auth_response_xml = self._GetSoapXml(AUTH_RESPONSE_FILE_LOCATION,
                                         response_values)

    http_headers = mock.MagicMock()
    http_headers.get.return_value = None
    expected_response = (200, 'OK', http_headers)

    with mock.patch('httplib.HTTPS') as mock_https:
      https_instance = mock_https.return_value
      https_instance.getreply.return_value = expected_response

      soap_responses = [StringIO.StringIO(response_xml),
                        StringIO.StringIO(auth_response_xml)]

      https_instance.getfile.side_effect = lambda *x: soap_responses.pop()

      login_wsdl_data = open(LOGIN_WSDL_FILE_LOCATION).read() % {'version': DEFAULT_API_VERSION}
      with mock.patch('urllib.urlopen') as mock_urlopen:
        mock_urlopen.return_value = StringIO.StringIO(login_wsdl_data)

        page = placement_service.GetPlacementTypes()

      # Ensure that the SOAP request matches the expected output.
      self.assertEqual(_RequestMatcher(expected_auth_request, True),
                       https_instance.send.call_args_list[0])
      self.assertEqual(_RequestMatcher(expected_request, False),
                       https_instance.send.call_args_list[1])

      # Ensure that we set the OAuth2 HTTP header.
      self.assertTrue(mock.call('Authorization', 'Bearer %s' % ACCESS_TOKEN) in
                      https_instance.putheader.call_args_list)

    return page

  def _MakeSoapRequest_ExpiredToken(self, placement_service):
    """Makes a "getPlacementTypes" request against the DFA placement service.

    All of the network interactions are mocked out. This method returns an
    expired token error to the SOAP call and tests that the library will refresh
    the token and retry the request.

    Args:
      placement_service: adspygoogle.adwords.GenericDfaService.GenericDfaService
          A service proxy for the DFA placement service.

    Returns:
      tuple The result set from the getPlacementTypes operation.
    """
    request_values = {
        'appName': USER_AGENT,
        'username': USER_NAME,
        'token': TOKEN,
        'libSig': LIB_SIG,
        'version': DEFAULT_API_VERSION
    }
    expected_request = self._GetSoapXml(REQUEST_FILE_LOCATION, request_values)
    expected_auth_request = self._GetSoapXml(AUTH_REQUEST_FILE_LOCATION,
                                             request_values)
    request_values['token'] = EXPIRED_TOKEN
    expected_failed_request = self._GetSoapXml(REQUEST_FILE_LOCATION,
                                               request_values)

    response_values = {
        'version': DEFAULT_API_VERSION,
        'token': TOKEN
    }
    response_xml = self._GetSoapXml(RESPONSE_FILE_LOCATION, response_values)
    expired_token_response_xml = self._GetSoapXml(
        EXPIRED_RESPONSE_FILE_LOCATION, response_values)
    auth_response_xml = self._GetSoapXml(AUTH_RESPONSE_FILE_LOCATION,
                                         response_values)

    http_headers = mock.MagicMock()
    http_headers.get.return_value = None
    expected_response = (200, 'OK', http_headers)

    with mock.patch('httplib.HTTPS') as mock_https:
      https_instance = mock_https.return_value
      https_instance.getreply.return_value = expected_response

      soap_responses = [StringIO.StringIO(response_xml),
                        StringIO.StringIO(auth_response_xml),
                        StringIO.StringIO(expired_token_response_xml)]

      https_instance.getfile.side_effect = lambda *x: soap_responses.pop()

      login_wsdl_data = open(LOGIN_WSDL_FILE_LOCATION).read() % {'version': DEFAULT_API_VERSION}
      with mock.patch('urllib.urlopen') as mock_urlopen:
        mock_urlopen.return_value = StringIO.StringIO(login_wsdl_data)

        page = placement_service.GetPlacementTypes()

      # Ensure that the SOAP request matches the expected output.
      self.assertEqual(_RequestMatcher(expected_failed_request, False),
                       https_instance.send.call_args_list[0])
      self.assertEqual(_RequestMatcher(expected_auth_request, True),
                       https_instance.send.call_args_list[1])
      self.assertEqual(_RequestMatcher(expected_request, False),
                       https_instance.send.call_args_list[2])

      # Ensure that we set the OAuth2 HTTP header.
      self.assertTrue(mock.call('Authorization', 'Bearer %s' % ACCESS_TOKEN) in
                      https_instance.putheader.call_args_list)

    return page

  def _GetSoapXml(self, file_location, template_values):
    raw_soap = open(file_location).read()
    return raw_soap % template_values


class _RequestMatcher(object):

  """Ensures that a SOAP request is equivalent to the expected request.

  For a definition of what we mean by equivalence, see the __eq__ function.
  """

  # The SOAP environment namespace used for extracting the SOAP header.
  SOAP_ENV_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
  WSSE_NS = ('http://docs.oasis-open.org/wss/2004/01/'
             'oasis-200401-wss-wssecurity-secext-1.0.xsd')

  def __init__(self, expected_xml, login_request):
    """Initializes a _RequestMatcher.

    Args:
      expected_xml: string The XML of the expected SOAP request.
      login_request: bool Whether this is a login service request.
    """
    self.expected_xml = expected_xml
    self.login_request = login_request

  def __str__(self):
    return self.expected_xml

  def __repr__(self):
    return '_RequestMatcher(%s)' % str(self)

  def __eq__(self, request_call):
    """Tests that the given SOAP request is equivalent to the expected request.

    In our context, equivalent means:
    1) With the exception of the SOAP header and its descendants, all XML is
       exactly identical, including the ordering of elements. AdWords enforces
       that all elements are in a proper order.
    2) The SOAP headers contain the same number of children, these children have
       identical tags, and all grandchildren of the two SOAP headers are
       identical, but the order of the children and grandchildren does not have
       to be identical.

    Args:
      request_call: mock.call The method call made by the library.

    Returns:
      boolean: Whether the given SOAP request XML is equivalent to the expected
      SOAP request.
    """
    request_args, request_kargs = request_call
    if len(request_args) != 1 or request_kargs:
      return False
    actual_xml = request_args[0]
    actual_tree = ElementTree.fromstring(actual_xml)
    expected_tree = ElementTree.fromstring(self.expected_xml)

    actual_request_header = actual_tree.find('{%s}Header' % self.SOAP_ENV_NS)
    expected_request_header = expected_tree.find('{%s}Header' %
                                                 self.SOAP_ENV_NS)

    actual_tree.remove(actual_request_header)
    expected_tree.remove(expected_request_header)

    return (self._CompareSoapHeaders(actual_request_header,
                                     expected_request_header) and
            self._CompareRequestMinusHeader(actual_tree, expected_tree))

  def _CompareRequestMinusHeader(self, actual_tree, expected_tree):
    """Compares two XML trees for equivalence.

    By equivalence, we check that the string representations are identical. This
    enforces that the order of elements is always the same.

    Args:
      actual_tree: xml.etree.ElementTree The tree of the actual request with the
                   SOAP header node removed.
      expected_tree: xml.etree.ElementTree The tree of the expected request with
                     the SOAP header node removed.

    Returns:
      boolean Whether the trees were equivalent.
    """
    return (ElementTree.tostring(actual_tree) ==
            ElementTree.tostring(expected_tree))

  def _CompareSoapHeaders(
      self, actual_header_node, expected_header_node):
    """Compares two SOAP headers for equivalence.

    By equivalence, we check that the two SOAP headers contain the same amount
    of children, that the RequestHeader children are identical, and that the
    WSSE headers contain identical grandchildren along with identical child
    tags. We do not enforce that the children, grandchildren, or
    great-grandchildren are in the same order.

    Args:
      actual_header_node: xml.etree.ElementTree The node of the actual SOAP
                          header.
      expected_header_node: xml.etree.ElementTree The node of the expected SOAP
                            header.

    Returns:
      boolean Whether the headers were equivalent.
    """
    same_length = len(actual_header_node) == len(expected_header_node)

    actual_request_header = actual_header_node.find('./RequestHeader')
    expected_request_header = expected_header_node.find('./RequestHeader')

    actual_wsse_header = actual_header_node.find(
        './{%s}Security' % self.WSSE_NS)
    expected_wsse_header = expected_header_node.find(
        './{%s}Security' % self.WSSE_NS)

    identical_request_headers = (ElementTree.tostring(actual_request_header) ==
                                 ElementTree.tostring(expected_request_header))

    if actual_wsse_header is not None and expected_wsse_header is not None:
      equivalent_wsse_headers = (
          set([ElementTree.tostring(grandchild) for grandchild in
               actual_wsse_header.findall('./*/*')]) ==
          set([ElementTree.tostring(grandchild) for grandchild in
               expected_wsse_header.findall('./*/*')]) and
          actual_wsse_header.find('./*').tag ==
          expected_wsse_header.find('./*').tag)
    else:
      equivalent_wsse_headers = False

    return (same_length and identical_request_headers and
            (equivalent_wsse_headers or self.login_request))


if __name__ == '__main__':
  unittest.main()
