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

"""Unit tests to cover Client."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join('..', '..', '..'))


from adspygoogle.common.Client import _DEFAULT_CONFIG
from adspygoogle.common.Client import Client
from adspygoogle.common.Errors import ValidationError


class ClientTest(unittest.TestCase):

  """Tests for the adspygoogle.common.Client module."""

  def setUp(self):
    """Initialize a Client to test with."""
    self.client = Client()

  def testLoadAuthCredentials_ClientLogin(self):
    """Tests the _LoadAuthCredentials function."""
    _, filename = tempfile.mkstemp()
    auth_credentials = {
        'username': 'Joseph',
        'password': 'DiLallo'
    }
    with open(filename, 'w') as handle:
      pickle.dump(auth_credentials, handle)

    try:
      Client.auth_pkl = filename
      self.assertEqual(self.client._LoadAuthCredentials(), auth_credentials)
    finally:
      Client.auth_pkl = ''

  def testLoadAuthCredentials_OAuth2(self):
    """Tests the _LoadAuthCredentials function."""
    _, filename = tempfile.mkstemp()
    client_id = 'id1234id',
    client_secret = 'shhh,itsasecret',
    refresh_token = '1/not_a_refresh_token'
    auth_credentials = {
        'clientId': client_id,
        'clientSecret': client_secret,
        'refreshToken': refresh_token
    }
    with open(filename, 'w') as handle:
      pickle.dump(auth_credentials, handle)

    try:
      Client.auth_pkl = filename
      read_credentials = self.client._LoadAuthCredentials()
      self.assertEqual(read_credentials['oauth2credentials'].refresh_token,
                       refresh_token)
      self.assertEqual(read_credentials['oauth2credentials'].client_secret,
                       client_secret)
      self.assertEqual(read_credentials['oauth2credentials'].client_id,
                       client_id)
      self.assertTrue('clientId' not in read_credentials)
      self.assertTrue('clientSecret' not in read_credentials)
      self.assertTrue('refreshToken' not in read_credentials)
    finally:
      Client.auth_pkl = ''

  def testLoadAuthCredentials_noPickle(self):
    """Tests the _LoadAuthCredentials function."""
    try:
      self.client._LoadAuthCredentials()
      self.fail('Exception should have been thrown.')
    except ValidationError, e:
      self.assertEqual(str(e), 'Authentication data is missing.')

  def testWriteUpdatedAuthValue(self):
    """Tests the _WriteUpdatedAuthValue function."""
    _, filename = tempfile.mkstemp()
    auth_credentials = {
        'username': 'Joseph',
        'password': 'DiLallo'
    }
    with open(filename, 'w') as handle:
      pickle.dump(auth_credentials, handle)

    try:
      Client.auth_pkl = filename
      self.client._WriteUpdatedAuthValue('password', 'new password')

      with open(filename, 'r') as handle:
        self.assertEqual(pickle.load(handle),
                         {'username': 'Joseph', 'password': 'new password'})
    finally:
      Client.auth_pkl = ''

  def testLoadConfigValues(self):
    """Tests the _LoadConfigValues function."""
    _, filename = tempfile.mkstemp()
    config_values = {
        'debug': 'yes plz',
        'compress': 'crunch'
    }
    with open(filename, 'w') as handle:
      pickle.dump(config_values, handle)

    try:
      Client.config_pkl = filename
      self.assertEqual(self.client._LoadConfigValues(), config_values)
    finally:
      Client.config_pkl = ''

  def testLoadConfigValues_noPickle(self):
    """Tests the _LoadConfigValues function."""
    self.assertEqual(self.client._LoadConfigValues(), {})

  def testSetMissingDefaultConfigValues(self):
    """Tests the _SetMissingDefaultConfigValues function."""
    self.assertEqual(self.client._SetMissingDefaultConfigValues(),
                     _DEFAULT_CONFIG)
    self.assertEqual(self.client._SetMissingDefaultConfigValues({}),
                     _DEFAULT_CONFIG)

    # Ensure it doesn't overwrite values which exist already
    partial_config = {
        'xml_parser': '2',
        'debug': 'y',
        'xml_log': 'y',
        'request_log': 'y',
        'auth_token_epoch': 15000,
        'auth_type': 'value',
        'pretty_xml': 'n',
    }
    expected_config = _DEFAULT_CONFIG.copy()
    for key in partial_config:
      expected_config[key] = partial_config[key]

    self.assertEqual(self.client._SetMissingDefaultConfigValues(partial_config),
                     expected_config)


if __name__ == '__main__':
  unittest.main()
