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

"""Tests to cover ReportDownloader."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import datetime
import os
import StringIO
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest
import urllib2

import mock
from oauth2client.client import OAuth2Credentials

from adspygoogle import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.AdWordsErrors import AdWordsReportError


class ReportDownloaderTest(unittest.TestCase):
  """Tests for ReportDownloader."""

  def setUp(self):
    """Prepare unittest."""
    with mock.patch('adspygoogle.adwords.util.XsdToWsdl.CreateWsdlFromXsdUrl'):
      client = AdWordsClient(headers={'authToken': 'AUTH TOKEN',
                                      'userAgent': 'USER AGENT',
                                      'developerToken': 'DEV TOKEN',
                                      'email': 'SOME@EMAIL.COM',
                                      'password': 'shhhh it is a secret!'})
      self.service = client.GetReportDownloader()

      credentials = OAuth2Credentials(
          'ACCESS_TOKEN', 'client_id', 'client_secret', 'refresh_token', None,
          'uri', 'user_agent')
      client_oauth2 = AdWordsClient(headers={'oauth2credentials': credentials,
                                             'userAgent': 'USER AGENT',
                                             'developerToken': 'DEV TOKEN'})
      self.service_oauth2 = client_oauth2.GetReportDownloader()

  def _ThrowErrorFromMakeRequest(self, payload_contents):
    """A test helper function to mock receiving an error during __MakeRequest.

    Args:
      payload_contents: str The payload to be returned with the HTTPError

    Raises:
      AdWordsError: The error returned from __MakeRequest
    """
    headers = mock.Mock()
    headers.headers = {'test': 'this'}
    payload = StringIO.StringIO()
    payload.write(payload_contents)
    payload.seek(0)
    adwords_report_response = urllib2.HTTPError(
        'url', '400', 'Bad Request', headers, payload)

    def RaiseMyError(*unused_args):
      raise adwords_report_response

    urllib2.urlopen = mock.Mock(side_effect=RaiseMyError)

    self.service._ReportDownloader__MakeRequest('url', payload='nothing')

  def testHandleXmlError(self):
    payload = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<reportDownloadError><ApiError><type>'
               'QueryError.INVALID_FROM_CLAUSE</type><trigger>Joseph'
               '</trigger><fieldPath>one.two.three</fieldPath></ApiError>'
               '</reportDownloadError>')
    try:
      self._ThrowErrorFromMakeRequest(payload)
      self.fail('Exception should have been thrown.')
    except AdWordsReportError, error:
      self.assertEquals('400', error.http_code)
      self.assertEquals('QueryError.INVALID_FROM_CLAUSE', error.type)
      self.assertEquals('Joseph', error.trigger)
      self.assertEquals('one.two.three', error.field_path)

  def testHandleUnknownError(self):
    payload = ('This is not a recognized error. It should appear unaltered in '
               'the error raised.')
    try:
      self._ThrowErrorFromMakeRequest(payload)
    except AdWordsError, e:
      self.assertTrue(payload in str(e))

  def testCheckForXmlError_withError(self):
    xml_message = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<reportDownloadError><ApiError><type>'
                   'QueryError.INVALID_FROM_CLAUSE</type><trigger>Joseph'
                   '</trigger><fieldPath>one.two\n.three</fieldPath></ApiError>'
                   '</reportDownloadError>')
    try:
      self.service._ReportDownloader__CheckForXmlError('400', xml_message)
      self.fail('Exception should have been thrown.')
    except AdWordsReportError, error:
      self.assertEquals('400', error.http_code)
      self.assertEquals('QueryError.INVALID_FROM_CLAUSE', error.type)
      self.assertEquals('Joseph', error.trigger)
      self.assertEquals('one.two\n.three', error.field_path)

  def testCheckForXmlError_noError(self):
    self.service._ReportDownloader__CheckForXmlError(
        '400', 'This is not an error XML message')

  def testGenerateHeaders_oAuth2(self):
    expected_headers = {
        'User-Agent': '%s,gzip' % 'USER AGENT',
        'Authorization': 'Bearer ACCESS_TOKEN',
        'returnMoneyInMicros': 'false',
        'developerToken': 'DEV TOKEN',
        'Content-Encoding': 'gzip',
        'Accept-Encoding': 'gzip'
    }

    self.assertEqual(
        expected_headers,
        self.service_oauth2._ReportDownloader__GenerateHeaders(False))

  def testCheckAuthentication_usingOAuth_refresh(self):
    credentials = mock.Mock()
    self.service_oauth2._headers['oauth2credentials'] = credentials
    rvals = {
        'token_expiry': datetime.datetime(1980, 1, 1, 12)
    }
    credentials.configure_mock(**rvals)

    self.service_oauth2._CheckAuthentication()

    self.assertTrue(credentials.refresh.called)

  def testCheckAuthentication_usingOAuth_noRefresh(self):
    credentials = mock.Mock()
    self.service_oauth2._headers['oauth2credentials'] = credentials
    rvals = {
        'token_expiry': datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    }
    credentials.configure_mock(**rvals)

    self.service_oauth2._CheckAuthentication()

    self.assertFalse(credentials.refresh.called)

  def testCheckAuthentication_clientLogin_refresh(self):
    old_token = self.service._headers['authToken']
    old_epoch = self.service._config['auth_token_epoch']
    del self.service._headers['authToken']
    del self.service._config['auth_token_epoch']
    try:
      with mock.patch('adspygoogle.common.Utils.GetAuthToken'
                     ) as mock_get_token:
        self.service._CheckAuthentication()
        self.assertTrue(mock_get_token.called)
    finally:
      self.service._headers['authToken'] = old_token
      self.service._config['auth_token_epoch'] = old_epoch

  def testCheckAuthentication_clientLogin_noRefresh(self):
    with mock.patch('adspygoogle.common.Utils.GetAuthToken') as mock_get_token:
      self.service._CheckAuthentication()
      self.assertFalse(mock_get_token.called)

  def testMakeRequestUnexpectedError(self):
    """Tests that ReportDownloader handles any error during __MakeRequest."""
    reason = 'Key error!'
    exception1 = KeyError(reason)

    def RaiseMyError(*unused_args):
      raise exception1
    urllib2.urlopen = mock.Mock(side_effect=RaiseMyError)

    try:
      self.service._ReportDownloader__MakeRequest('url', payload='nothing')
    except KeyError, e:
      self.assertIs(exception1, e)


if __name__ == '__main__':
  unittest.main()
