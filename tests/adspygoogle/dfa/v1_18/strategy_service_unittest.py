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

"""Unit tests to cover StrategyService."""

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


class StrategyServiceTestV1_18(unittest.TestCase):

  """Unittest suite for StrategyService using v1_18."""

  SERVER = SERVER_V1_18
  VERSION = VERSION_V1_18
  client.debug = False
  service = None
  strategy_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetStrategyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetPlacementStrategy(self):
    """Test whether we can fetch a placement strategy by id"""
    if self.__class__.strategy_id == '0':
      self.testSavePlacementStrategy()
    strategy_id = self.__class__.strategy_id
    self.assert_(isinstance(self.__class__.service.GetPlacementStrategy(
        strategy_id), tuple))

  def testSavePlacementStrategy(self):
    """Test whether we can save a placement strategy"""
    placement_strategy = {
        'name': 'Placement Strategy #%s' % Utils.GetUniqueName(),
        'id' : '-1'
    }
    placement_strategy = self.__class__.service.SavePlacementStrategy(
        placement_strategy)
    self.__class__.strategy_id = placement_strategy[0]['id']
    self.assert_(isinstance(placement_strategy, tuple))

  def testGetPlacementStrategiesByCriteria(self):
    """Test whether we can fetch placement strategies by criteria."""
    if self.__class__.strategy_id == '0':
      self.testSavePlacementStrategy()
    search_criteria = {
        'ids': [self.__class__.strategy_id]
    }
    self.__class__.strategy_id = \
        self.__class__.service.GetPlacementStrategiesByCriteria(
            search_criteria)[0]['records'][0]['id']

  def testDeletePlacementStrategy(self):
    """Test whether we can delete a placement strategy"""
    if self.__class__.strategy_id == '0':
      self.testSavePlacementStrategy()
    self.assertEqual(self.__class__.service.DeletePlacementStrategy(
        self.__class__.strategy_id), None)
    self.__class__.strategy_id = '0'


if __name__ == '__main__':
  unittest.main()
