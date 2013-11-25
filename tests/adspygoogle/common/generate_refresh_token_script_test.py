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

"""Unit tests to cover generate_refresh_token."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import StringIO
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from scripts.adspygoogle.common import generate_refresh_token


SYS_STDOUT = sys.stdout


class GenerateRefreshTokenTest(unittest.TestCase):

  """Tests for the adspygoogle.common.generate_refresh_token script."""

  def testGenerateRefreshToken_AdWordsOrAdX(self):
    """Tests the generate_refresh_token script for AdWords/AdX."""
    raw_input_rvals = {
        'Client ID: ': 'myclientid',
        'Client Secret: ': 'myclientsecret',
        'Please enter a number: ': '1',
        'Code: ': 'mycode'
    }
    mock_credential = mock.Mock()
    mock_credential.refresh_token = 'myrefreshtoken'

    def RawInputReturnValues(*args, **unused_kwargs):
      return raw_input_rvals[args[0]]

    with mock.patch('__builtin__.raw_input') as mock_raw_input, mock.patch(
        'oauth2client.client.OAuth2WebServerFlow') as mock_flow:
      mock_raw_input.side_effect = RawInputReturnValues
      flow_instance = mock_flow.return_value
      flow_instance.step2_exchange.return_value = mock_credential

      output = StringIO.StringIO()

      sys.stdout = output
      try:
        generate_refresh_token.main()
      finally:
        sys.stdout = SYS_STDOUT

      mock_flow.assert_called_once_with(
          client_id='myclientid', client_secret='myclientsecret',
          scope=generate_refresh_token.PRODUCT_TO_OAUTH_SCOPE[
              'AdWords / Ad Exchange Buyer'],
          user_agent='Ads Python Client Library',
          redirect_uri='urn:ietf:wg:oauth:2.0:oob')
      flow_instance.step1_get_authorize_url.assert_called_once_with()
      flow_instance.step2_exchange.assert_called_once_with('mycode')

      self.assertTrue(output.getvalue().strip().endswith(
          'Your refresh token is: myrefreshtoken'))
      output.close()

  def testGenerateRefreshToken_DFA(self):
    """Tests the generate_refresh_token script for DFA."""
    raw_input_rvals = {
        'Client ID: ': 'myclientid',
        'Client Secret: ': 'myclientsecret',
        'Please enter a number: ': '2',
        'Code: ': 'mycode'
    }
    mock_credential = mock.Mock()
    mock_credential.refresh_token = 'myrefreshtokendfa'

    def RawInputReturnValues(*args, **unused_kwargs):
      return raw_input_rvals[args[0]]

    with mock.patch('__builtin__.raw_input') as mock_raw_input, mock.patch(
        'oauth2client.client.OAuth2WebServerFlow') as mock_flow:
      mock_raw_input.side_effect = RawInputReturnValues
      flow_instance = mock_flow.return_value
      flow_instance.step2_exchange.return_value = mock_credential

      output = StringIO.StringIO()

      sys.stdout = output
      try:
        generate_refresh_token.main()
      finally:
        sys.stdout = SYS_STDOUT

      mock_flow.assert_called_once_with(
          client_id='myclientid', client_secret='myclientsecret',
          scope=generate_refresh_token.PRODUCT_TO_OAUTH_SCOPE[
              'DoubleClick for Advertisers'],
          user_agent='Ads Python Client Library',
          redirect_uri='urn:ietf:wg:oauth:2.0:oob')
      flow_instance.step1_get_authorize_url.assert_called_once_with()
      flow_instance.step2_exchange.assert_called_once_with('mycode')

      self.assertTrue(output.getvalue().strip().endswith(
          'Your refresh token is: myrefreshtokendfa'))
      output.close()

  def testGenerateRefreshToken_DFP(self):
    """Tests the generate_refresh_token script for DFP."""
    raw_input_rvals = {
        'Client ID: ': 'myclientid',
        'Client Secret: ': 'myclientsecret',
        'Please enter a number: ': '3',
        'Code: ': 'mycode'
    }
    mock_credential = mock.Mock()
    mock_credential.refresh_token = 'myrefreshtokendfp'

    def RawInputReturnValues(*args, **unused_kwargs):
      return raw_input_rvals[args[0]]

    with mock.patch('__builtin__.raw_input') as mock_raw_input, mock.patch(
        'oauth2client.client.OAuth2WebServerFlow') as mock_flow:
      mock_raw_input.side_effect = RawInputReturnValues
      flow_instance = mock_flow.return_value
      flow_instance.step2_exchange.return_value = mock_credential

      output = StringIO.StringIO()

      sys.stdout = output
      try:
        generate_refresh_token.main()
      finally:
        sys.stdout = SYS_STDOUT

      mock_flow.assert_called_once_with(
          client_id='myclientid', client_secret='myclientsecret',
          scope=generate_refresh_token.PRODUCT_TO_OAUTH_SCOPE[
              'DoubleClick for Publishers'],
          user_agent='Ads Python Client Library',
          redirect_uri='urn:ietf:wg:oauth:2.0:oob')
      flow_instance.step1_get_authorize_url.assert_called_once_with()
      flow_instance.step2_exchange.assert_called_once_with('mycode')

      self.assertTrue(output.getvalue().strip().endswith(
          'Your refresh token is: myrefreshtokendfp'))
      output.close()


if __name__ == '__main__':
  unittest.main()
