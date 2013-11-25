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

"""Unit tests to cover CreativeGroupService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa.v1_18 import client
from tests.adspygoogle.dfa.v1_18 import HTTP_PROXY
from tests.adspygoogle.dfa.v1_18 import SERVER_V1_18
from tests.adspygoogle.dfa.v1_18 import VERSION_V1_18


class CreativeGroupServiceTestV1_18(unittest.TestCase):

  """Unittest suite for CreativeGroupService using v1_18."""

  SERVER = SERVER_V1_18
  VERSION = VERSION_V1_18
  client.debug = False
  service = None
  creative_group_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testGetCreativeGroup(self):
    """Test whether we can fetch a creative group by id"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    creative_group_id = self.__class__.creative_group_id
    self.assert_(isinstance(self.__class__.service.GetCreativeGroup(
        creative_group_id), tuple))

  def testSaveCreativeGroup(self):
    """Test whether we can save a creative group"""
    creative_group = {
        'name': 'Creative Group #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'groupNumber' : '1',
        'id' : '-1'
    }
    creative_group = self.__class__.service.SaveCreativeGroup(
        creative_group)
    self.__class__.creative_group_id = creative_group[0]['id']
    self.assert_(isinstance(creative_group, tuple))

  def testGetCreativeGroups(self):
    """Test whether we can fetch creative groups by criteria."""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    search_criteria = {
        'ids': [self.__class__.creative_group_id]
    }
    self.__class__.creative_group_id = self.__class__.service.GetCreativeGroups(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeGroup(self):
    """Test whether we can delete a creative group"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    self.assertEqual(self.__class__.service.DeleteCreativeGroup(
        self.__class__.creative_group_id), None)
    self.__class__.creative_group_id = '0'


if __name__ == '__main__':
  unittest.main()
