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

"""Integration test for issue #57.

Makes sure that SOAPpy packs operation arguments in the correct order.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import StringIO
import sys
import unittest
from xml.etree import ElementTree
sys.path.insert(0, os.path.join('..', '..', '..', '..'))


from adspygoogle.common.Errors import Error
from adspygoogle.dfp import DEFAULT_API_VERSION
from adspygoogle.dfp.DfpClient import DfpClient
import mock
from oauth2client.client import OAuth2Credentials



# Location of a cached WSDL to generate a service proxy from.
WSDL_FILE_LOCATION = os.path.join('..', 'data', 'line_item_service.wsdl')

# Values used for the application name, network code, and OAuth 2 access token
# in our test code.
APPLICATION_NAME = 'Issue 57'
NETWORK_CODE = 'NID123'
ACCESS_TOKEN = 'a1b2c3d4e5'

# Values we're actually checking: what method are we calling, and what order
# should its arguments be in.
METHOD_NAME = 'performLineItemAction'
EXPECTED_ARG_ORDER = ['lineItemAction', 'filterStatement']


class Issue57IntegrationTest(unittest.TestCase):

  """Tests thats Issue 57 has been correctly fixed."""

  def testIssue57(self):
    """Tests thats Issue 57 has been correctly fixed.

    Since this library is tightly integrated with SOAPpy, this test mocks out
    the HTTP level rather than the SOAPpy proxy level.
    """
    client = DfpClient(headers={
        'applicationName': APPLICATION_NAME,
        'networkId': NETWORK_CODE,
        'oauth2credentials': OAuth2Credentials(
            ACCESS_TOKEN, 'client_id', 'client_secret', 'refresh_token', None,
            'uri', 'user_agent')
    })

    line_item_service = self._CreateLineItemService(client)
    line_item_service._config['compress'] = False

    self._MakeSoapRequest(line_item_service)

  def _CreateLineItemService(self, client):
    """Creates a SOAP service proxy for the DFP LineItemService.

    All of the network interactions are mocked out.

    Args:
      client: adspygoogle.Dfp.DfpClient.DfpClient A client ready to make
              requests against the DFP API.

    Returns:
      adspygoogle.dfp.GenericDfpService.GenericDfpService A service proxy
      for the LineItemService.
    """
    wsdl_data = open(WSDL_FILE_LOCATION).read() % {'version': DEFAULT_API_VERSION}
    with mock.patch('urllib.urlopen') as mock_urlopen:
      mock_urlopen.return_value = StringIO.StringIO(wsdl_data)
      return client.GetLineItemService()

  def _MakeSoapRequest(self, line_item_service):
    """Makes a request against the DFP LineItemService.

    All of the network interactions are mocked out.

    Args:
      line_item_service:
          adspygoogle.dfp.GenericDfpService.GenericDfpService A
          service proxy for the DFP LineItemService.
    """
    values = [{
        'key': 'orderId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': '111165854'
        }
    }, {
        'key': 'status',
        'value': {
            'xsi_type': 'TextValue',
            'value': 'NEEDS_CREATIVES'
        }
    }]
    query = 'WHERE orderId = :orderId AND status = :status'

    http_headers = mock.MagicMock()
    http_headers.get.return_value = None
    expected_response = (200, 'OK', http_headers)

    with mock.patch('httplib.HTTPS') as mock_https:
      https_instance = mock_https.return_value
      https_instance.getreply.return_value = expected_response
      https_instance.getfile.return_value = StringIO.StringIO()

      try:
        getattr(line_item_service, METHOD_NAME)(
            {'type': 'ActivateLineItems'},
            {'query': query, 'values': values})[0]
      except Error:
        # We're not passing back a SOAP response to deserialize, so the call
        # errors out. We're only interested in the request, just keep going.
        pass

      # Ensure that the SOAP request has the operation arguments in the correct
      # order.
      https_instance.send.assert_called_with(_ArgumentChecker(
          METHOD_NAME, EXPECTED_ARG_ORDER))


class _ArgumentChecker(object):

  """Ensures that a SOAP request has the arguments in the expected order."""

  # The DFP namespace used for xpath searching.
  DFP_NS = 'https://www.google.com/apis/ads/publisher/%s' % DEFAULT_API_VERSION

  def __init__(self, operation_name, args_in_order):
    """Initializes an _ArgumentChecker.

    Args:
      operation_name: str The name of the operation in the SOAP request.
      args_in_order: list of str The name (see: XML tag) of the arguments to
                     this SOAP operation, in order.
    """
    self.operation_name = operation_name
    self.args_in_order = args_in_order

  def __eq__(self, actual_xml):
    """Tests that the given SOAP request has its arguments in order.

    Args:
      actual_xml: string The actual XML request made by the library.

    Returns:
      boolean: Whether the given SOAP request has its arguments in the correct
      order.
    """
    actual_tree = ElementTree.fromstring(actual_xml)
    operation_node = actual_tree.find('.//{%s}%s' % (self.DFP_NS,
                                                     self.operation_name))
    if (operation_node is None or
        len(operation_node.getchildren()) != len(self.args_in_order)):
      return False

    for i in range(len(self.args_in_order)):
      if (operation_node.getchildren()[i].tag !=
          '{%s}%s' % (self.DFP_NS, self.args_in_order[i])):
        return False

    return True


if __name__ == '__main__':
  unittest.main()
