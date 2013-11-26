#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover AdvertiserService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa.v1_19 import client
from tests.adspygoogle.dfa.v1_19 import HTTP_PROXY
from tests.adspygoogle.dfa.v1_19 import SERVER_V1_19
from tests.adspygoogle.dfa.v1_19 import VERSION_V1_19


class AdvertiserServiceTestV1_19(unittest.TestCase):

  """Unittest suite for AdvertiserService using v1_19."""

  SERVER = SERVER_V1_19
  VERSION = VERSION_V1_19
  client.debug = False
  service = None
  advertiser1 = None
  advertiser2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testDeleteAdvertiser(self):
    """Test whether we can delete an advertiser."""
    if self.__class__.advertiser2 is None:
      self.testSaveAdvertiser()
    self.assertEqual(self.__class__.service.DeleteAdvertiser(
        self.__class__.advertiser2['id']), None)

  def testGetAdvertisers(self):
    """Test whether we can fetch advertisers."""
    if self.__class__.advertiser1 is None:
      self.testSaveAdvertiser()
    search_criteria = {
        'ids': [self.__class__.advertiser1['id']]
    }
    self.__class__.advertiser_id = self.__class__.service.GetAdvertisers(
        search_criteria)[0]['records'][0]['id']

  def testSaveAdvertiser(self):
    """Test whether we can create an advertiser."""
    advertiser = {
        'name': 'Advertiser #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser1 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))

    advertiser = {
        'name': '广告客户 #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser2 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))


if __name__ == '__main__':
  unittest.main()
