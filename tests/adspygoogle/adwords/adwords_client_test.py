#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unit tests to cover AdWordsClient."""

__author__ = ('api.kwinter@gmail.com (Kevin Winter)',
              'api.jdilallo@gmail.com (Joseph DiLallo)')

import os
import StringIO
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common.Errors import ValidationError


DEFAULT_HEADERS = {
    'userAgent': 'Foo Bar',
    'developerToken': 'devtoken'
}


class AdWordsClientValidationTest(unittest.TestCase):

  """Tests the validation logic when instantiating AdWordsClient."""

  def testEmailPassOnly(self):
    """Tests that specifying solely email & password works."""
    with mock.patch('adspygoogle.common.Utils.GetAuthToken') as mock_get_token:
      mock_get_token.return_value = 'FooBar'
      headers = DEFAULT_HEADERS.copy()
      headers['email'] = 'email@example.com'
      headers['password'] = 'password'
      client = AdWordsClient(headers=headers)
      self.assertEquals(client._headers['authToken'], 'FooBar')
      mock_get_token.assert_called_once_with(
          'email@example.com', 'password', mock.ANY, mock.ANY, mock.ANY,
          mock.ANY, mock.ANY)

  def testEmailPassOthersBlank(self):
    """Tests that email and password with other auth blank works."""
    with mock.patch('adspygoogle.common.Utils.GetAuthToken') as mock_get_token:
      mock_get_token.return_value = 'FooBar'
      headers = DEFAULT_HEADERS.copy()
      headers['email'] = 'email@example.com'
      headers['password'] = 'password'
      headers['authToken'] = ''
      headers['oauth_credentials'] = None
      client = AdWordsClient(headers=headers)
      self.assertEquals(client._headers['authToken'], 'FooBar')
      mock_get_token.assert_called_once_with(
          'email@example.com', 'password', mock.ANY, mock.ANY, mock.ANY,
          mock.ANY, mock.ANY)

  def testAuthTokenOnly(self):
    """Tests that specifying solely authtoken works."""
    headers = DEFAULT_HEADERS.copy()
    headers['authToken'] = 'MyToken'
    client = AdWordsClient(headers=headers)
    self.assertEquals(client._headers['authToken'], 'MyToken')

  def testAuthTokenOthersBlank(self):
    """Tests that authToken with other auth blank works."""
    headers = DEFAULT_HEADERS.copy()
    headers['authToken'] = 'MyToken'
    headers['email'] = ''
    headers['password'] = ''
    headers['oauth_credentials'] = None
    client = AdWordsClient(headers=headers)
    self.assertEquals(client._headers['authToken'], 'MyToken')

  def testOAuth2CredentialsOnly(self):
    """Tests that specifying solely oauth_credentials works."""
    headers = DEFAULT_HEADERS.copy()
    headers['oauth2credentials'] = 'credential!'
    client = AdWordsClient(headers=headers)
    self.assertTrue(client.oauth2credentials)

  def testOAuthCredentialsOthersBlank(self):
    """Tests that oauth_credentials with other auth blank works."""
    headers = DEFAULT_HEADERS.copy()
    headers['oauth2credentials'] = 'credential!'
    headers['email'] = ''
    headers['password'] = ''
    headers['authToken'] = ''
    client = AdWordsClient(headers=headers)
    self.assertTrue(client.oauth2credentials)

  def testNonStrictThrowsValidationError(self):
    """Tests that even when using non-strict mode, we still raise a
    ValidationError when no auth credentials are provided."""
    headers = DEFAULT_HEADERS.copy()
    config = {'strict': 'n'}

    def Run():
      _ = AdWordsClient(headers=headers, config=config)
    self.assertRaises(ValidationError, Run)


class AdWordsClientCaptchaHandlingTest(unittest.TestCase):

  """Tests the captcha handling logic."""
  CAPTCHA_CHALLENGE = '''Url=http://www.google.com/login/captcha
Error=CaptchaRequired
CaptchaToken=DQAAAGgA...dkI1LK9
CaptchaUrl=Captcha?ctoken=HiteT4b0Bk5Xg18_AcVoP6-yFkHPibe7O9EqxeiI7lUSN'''
  SUCCESS = '''SID=DQAAAGgA...7Zg8CTN
LSID=DQAAAGsA...lk8BBbG
Auth=DQAAAGgA...dk3fA5N'''

  def testCaptchaHandling(self):
    headers = DEFAULT_HEADERS.copy()
    headers['email'] = 'email@example.com'
    headers['password'] = 'password'
    client = None
    try:
      with mock.patch('urllib2.urlopen') as mock_urlopen:
        mock_urlopen.return_value = StringIO.StringIO(self.CAPTCHA_CHALLENGE)
        client = AdWordsClient(headers=headers)
      self.fail('Expected a CaptchaError to be thrown')
    except ValidationError, e:
      with mock.patch('urllib2.urlopen') as mock_urlopen:
        mock_urlopen.return_value = StringIO.StringIO(self.SUCCESS)
        client = AdWordsClient(headers=headers,
                               login_token=e.root_cause.captcha_token,
                               login_captcha='foo bar')
        self.assertEquals(client._headers['authToken'], 'DQAAAGgA...dk3fA5N')


class AdWordsClientServiceTest(unittest.TestCase):
  """Tests for retrieving SOAP services via AdWordsClient."""

  def setUp(self):
    """Prepare unittest."""
    self.client = AdWordsClient(headers={'authToken': 'AUTH TOKEN',
                                         'userAgent': 'USER AGENT',
                                         'developerToken': 'DEV TOKEN'})

  def testGetBudgetService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetBudgetService()
      self.assertEquals('BudgetService', service._service_name)

  def testGetAdGroupFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetAdGroupFeedService()
      self.assertEquals('AdGroupFeedService', service._service_name)

  def testGetCampaignFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetCampaignFeedService()
      self.assertEquals('CampaignFeedService', service._service_name)

  def testGetFeedItemService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetFeedItemService()
      self.assertEquals('FeedItemService', service._service_name)

  def testGetFeedMappingService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetFeedMappingService()
      self.assertEquals('FeedMappingService', service._service_name)

  def testGetFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetFeedService()
      self.assertEquals('FeedService', service._service_name)

  def testGetCampaignSharedSetService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetCampaignSharedSetService()
      self.assertEquals('CampaignSharedSetService', service._service_name)

  def testGetSharedSetService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetSharedSetService()
      self.assertEquals('SharedSetService', service._service_name)

  def testGetSharedCriterionService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetSharedCriterionService()
      self.assertEquals('SharedCriterionService', service._service_name)

  def testGetAdGroupBidModifierService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetAdGroupBidModifierService()
      self.assertEquals('AdGroupBidModifierService', service._service_name)

  def testGetOfflineConversionFeedService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetOfflineConversionFeedService()
      self.assertEquals('OfflineConversionFeedService', service._service_name)


if __name__ == '__main__':
  unittest.main()
