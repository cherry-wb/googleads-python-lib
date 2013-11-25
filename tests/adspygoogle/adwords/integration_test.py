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

"""Integration test for end-to-end usage of the AdWords API."""

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


from adspygoogle.adwords import DEFAULT_API_VERSION
from adspygoogle.adwords import LIB_SIG
from adspygoogle.adwords.AdWordsClient import AdWordsClient
import mock
from oauth2client.client import OAuth2Credentials



# Location of a cached WSDL to generate a service proxy from.
WSDL_FILE_LOCATION = os.path.join('data', 'campaign_service.wsdl')
# Location of the cached expected SOAP request XML, with some Python string
# formatting operations inside for better flexibility.
REQUEST_FILE_LOCATION = os.path.join('data', 'integration_test_request.xml')
# Location of the cached expected SOAP response XML.
RESPONSE_FILE_LOCATION = os.path.join('data', 'integration_test_response.xml')
# Deserialized value of the page object stored in the cached SOAP response.
EXPECTED_PAGE = {
    'totalNumEntries': '5',
    'totalBudget': {
        'amount': {
            'ComparableValue_Type': 'Money',
            'microAmount': '0'
        },
        'period': 'DAILY'
    },
    'Page_Type': 'CampaignPage',
    'entries': [
        {'status': 'DELETED', 'campaignStats': {'network': 'ALL',
                                                'Stats_Type': 'CampaignStats'},
         'name': 'Deleted on 20120927 07:45:35.088913',
         'frequencyCap': {'impressions': '0'}, 'id': '90835362'},
        {'status': 'PAUSED', 'campaignStats': {'network': 'ALL',
                                               'Stats_Type': 'CampaignStats'},
         'name': 'Interplanetary Cruise banner #52338591982792012',
         'frequencyCap': {'impressions': '0'}, 'id': '90844362'},
        {'status': 'PAUSED', 'campaignStats': {'network': 'ALL',
                                               'Stats_Type': 'CampaignStats'},
         'name': 'Interplanetary Cruise #52254591982792012',
         'frequencyCap': {'impressions': '0'}, 'id': '90844482'},
        {'status': 'PAUSED', 'campaignStats': {'network': 'ALL',
                                               'Stats_Type': 'CampaignStats'},
         'name': 'Campaign #218532375582892012',
         'frequencyCap': {'impressions': '0'}, 'id': '91018842'},
        {'status': 'PAUSED', 'campaignStats': {'network': 'ALL',
                                               'Stats_Type': 'CampaignStats'},
         'name': 'Campaign #325634565682892012',
         'frequencyCap': {'impressions': '0'}, 'id': '91019082'}
    ]}

# Values used in our test code.
ACCESS_TOKEN = 'a1b2c3d4e5'
CLIENT_ID = 'id1234id'
CLIENT_SECRET = 'shhh,itsasecret'
REFRESH_TOKEN = '1/not_a_refresh_token'
OAUTH_URI = 'uri'
USER_AGENT = 'Integration Test'
DEVELOPER_TOKEN = 'devtoken'
CLIENT_CUSTOMER_ID = 'CCID123'


class AdWordsIntegrationTest(unittest.TestCase):

  """Tests end-to-end usage of the AdWords library."""

  def testWithPassedInCredential(self):
    """Tests the entire workflow of making a request against AdWords.

    Uses a credential passed in to the constructor.

    Since this library is tightly integrated with SOAPpy, this test mocks out
    the HTTP level rather than the SOAPpy proxy level.
    """
    oauth2_credential = self._CreateOAuth2Credential()

    client = self._CreateAdWordsClient(oauth2_credential)

    campaign_service = self._CreateCampaignService(client)
    campaign_service._config['compress'] = False

    page = self._MakeSoapRequest(campaign_service)

    # Assert that the serialized objects returned in the SOAP response
    # deserialize to the expected output. Also check that we correctly interpret
    # the operation and unit costs.
    self.assertEquals(EXPECTED_PAGE, page)
    self.assertEquals(8, client.GetOperations())

  def testWithCachedRefreshToken(self):
    """Tests the entire workflow of making a request against AdWords.

    Uses a cached refresh token to generate a credential.

    Since this library is tightly integrated with SOAPpy, this test mocks out
    the HTTP level rather than the SOAPpy proxy level.
    """
    directory = self._CreateConfigPickles()

    try:
      with mock.patch(
          'oauth2client.client.OAuth2Credentials.refresh') as mock_refresh:
        client = AdWordsClient(path=directory)

        self.assertEquals(CLIENT_ID, client.oauth2credentials.client_id)
        self.assertEquals(CLIENT_SECRET, client.oauth2credentials.client_secret)
        self.assertEquals(REFRESH_TOKEN, client.oauth2credentials.refresh_token)

        def SetAccessToken(unused_http):
          client.oauth2credentials.access_token = ACCESS_TOKEN
        mock_refresh.side_effect = SetAccessToken

        campaign_service = self._CreateCampaignService(client)
        page = self._MakeSoapRequest(campaign_service)

        # Assert that the serialized objects returned in the SOAP response
        # deserialize to the expected output. Also check that we correctly
        # interpret the operations.
        self.assertEquals(EXPECTED_PAGE, page)
        self.assertEquals(8, client.GetOperations())
        client.oauth2credentials.refresh.assert_called_once_with(mock.ANY)
    finally:
      shutil.rmtree(directory)

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
        'userAgent': USER_AGENT,
        'developerToken': DEVELOPER_TOKEN,
        'clientCustomerId': CLIENT_CUSTOMER_ID
    }
    config = {
        'compress': False
    }
    with open(os.path.join(directory, AdWordsClient.auth_pkl_name),
              'w') as handle:
      pickle.dump(auth_credentials, handle)

    with open(os.path.join(directory, AdWordsClient.config_pkl_name),
              'w') as handle:
      pickle.dump(config, handle)

    return directory

  def _CreateOAuth2Credential(self):
    """Creates an OAuth2 Credential for use authenticating against AdWords.

    We are not testing the oauth2client credential creation flow since our
    library does not wrap it. Instead, we are mimicking what a user who cached
    their OAuth2 credentials would do - create a credential from stored values.

    Returns:
      oauth2client.client.OAuth2Credentials The OAuth2 credential object used to
      authenticate against AdWords.
    """
    return OAuth2Credentials(
        ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, None,
        OAUTH_URI, USER_AGENT)

  def _CreateAdWordsClient(self, oauth2_credential):
    """Creates an AdWordsClient using the given OAuth2 credential.

    Args:
      oauth2_credential: oauth2client.client.OAuth2Credentials The credential
                         object this client will use to authenticate.

    Returns:
      adspygoogle.adwords.AdWordsClient.AdwordsClient A client ready to make
      requests against the AdWords API.
    """
    headers = {
        'userAgent': USER_AGENT,
        'developerToken': DEVELOPER_TOKEN,
        'clientCustomerId': CLIENT_CUSTOMER_ID,
        'oauth2credentials': oauth2_credential
    }
    return AdWordsClient(headers=headers)

  def _CreateCampaignService(self, client):
    """Creates a SOAP service proxy for the AdWords CampaignService.

    All of the network interactions are mocked out.

    Args:
      client: adspygoogle.adwords.AdwordsClient.AdWordsClient A client ready to
              make requests against the AdWords API.

    Returns:
      adspygoogle.adwords.GenericAdWordsService.GenericAdWordsService A service
      proxy for the CampaignService.
    """
    wsdl_data = open(WSDL_FILE_LOCATION).read() % {'version': DEFAULT_API_VERSION}
    with mock.patch('urllib.urlopen') as mock_urlopen:
      mock_urlopen.return_value = StringIO.StringIO(wsdl_data)
      return client.GetCampaignService()

  def _MakeSoapRequest(self, campaign_service):
    """Makes a "get" request against the AdWords CampaignService.

    All of the network interactions are mocked out.

    Args:
      campaign_service:
          adspygoogle.adwords.GenericAdWordsService.GenericAdWordsService A
          service proxy for the AdWords CampaignService.

    Returns:
      dict A page object returned from the CampaignService.get operation.
    """
    expected_request_values = {
        'userAgent': USER_AGENT,
        'developerToken': DEVELOPER_TOKEN,
        'clientCustomerId': CLIENT_CUSTOMER_ID,
        'libSig': LIB_SIG,
        'version': DEFAULT_API_VERSION
    }
    raw_expected_request = open(REQUEST_FILE_LOCATION).read()
    expected_request = raw_expected_request % expected_request_values

    expected_response_values = {
        'version': DEFAULT_API_VERSION
    }
    raw_response_xml = open(RESPONSE_FILE_LOCATION).read()
    response_xml = raw_response_xml % expected_response_values
    http_headers = mock.MagicMock()
    http_headers.get.return_value = None
    expected_response = (200, 'OK', http_headers)

    selector = {
        'fields': ['Id', 'Name', 'Status'],
        'paging': {
            'startIndex': '100',
            'numberResults': '100'
        },
        'predicates': [{
            'field': ''
        }]
    }

    with mock.patch('httplib.HTTPS') as mock_https:
      https_instance = mock_https.return_value
      https_instance.getreply.return_value = expected_response
      https_instance.getfile.return_value = StringIO.StringIO(response_xml)

      page = campaign_service.Get(selector)[0]

      # Ensure that the SOAP request matches the expected output.
      https_instance.send.assert_called_with(_RequestMatcher(expected_request))

      # Ensure that we set the OAuth2 HTTP header.
      self.assertTrue(mock.call('Authorization', 'Bearer %s' % ACCESS_TOKEN) in
                      https_instance.putheader.call_args_list)

    return page


class _RequestMatcher(object):

  """Ensures that a SOAP request is equivalent to the expected request.

  For a definition of what we mean by equivalence, see the __eq__ function.
  """

  # The SOAP environment namespace used for extracting the SOAP header.
  SOAP_ENV_NS = 'http://schemas.xmlsoap.org/soap/envelope/'

  def __init__(self, expected_xml):
    """Initializes a _RequestMatcher.

    Args:
      expected_xml: string The XML of the expected SOAP request.
    """
    self.expected_xml = expected_xml

  def __eq__(self, actual_xml):
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
      actual_xml: string The actual XML request made by the library.

    Returns:
      boolean: Whether the given SOAP request XML is equivalent to the expected
      SOAP request.
    """
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
    of children, that both headers contain children with the same tags, and that
    all of the header's grandchildren are identical. We do not enforce that the
    children or grandchildren are in the same order.

    Args:
      actual_header_node: xml.etree.ElementTree The node of the actual SOAP
                          header.
      expected_header_node: xml.etree.ElementTree The node of the expected SOAP
                            header.

    Returns:
      boolean Whether the headers were equivalent.
    """
    same_length = len(actual_header_node) == len(expected_header_node)
    same_child_tags = (set([child.tag for child in actual_header_node]) ==
                       set([child.tag for child in expected_header_node]))
    identical_grandchildren = (
        set([ElementTree.tostring(grandchild) for grandchild in
             actual_header_node.find('.//*')]) ==
        set([ElementTree.tostring(grandchild) for grandchild in
             expected_header_node.find('.//*')]))
    return same_length and same_child_tags and identical_grandchildren


if __name__ == '__main__':
  unittest.main()
