#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover inventory service examples."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.dfp.v201208.inventory_service import archive_ad_units
from examples.adspygoogle.dfp.v201208.inventory_service import create_ad_units
from examples.adspygoogle.dfp.v201208.inventory_service import get_ad_unit_hierarchy
from examples.adspygoogle.dfp.v201208.inventory_service import get_mobile_ad_unit_sizes
from examples.adspygoogle.dfp.v201208.inventory_service import get_top_level_ad_units
from examples.adspygoogle.dfp.v201208.inventory_service import update_ad_units
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import SERVER_V201208
from tests.adspygoogle.dfp import TEST_VERSION_V201208
from tests.adspygoogle.dfp import util
from tests.adspygoogle.dfp import VERSION_V201208


class InventoryServiceTest(unittest.TestCase):
  """Unittest suite for InventoryService."""

  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.__class__.loaded:
      self.__class__.effective_root_ad_unit_id = util.GetEffectiveRootAdUnitId(
          client, SERVER_V201208, VERSION_V201208)
      self.__class__.loaded = True

  def testArchiveAdUnits(self):
    """Test whether we can archive ad units."""
    archive_ad_units.main(client, self.__class__.effective_root_ad_unit_id)

  def testCreateAdUnits(self):
    """Test whether we can create ad units."""
    create_ad_units.main(client, self.__class__.effective_root_ad_unit_id)

  def testGetAdUnitHierarchy(self):
    """Test whether we can get an ad unit hierarchy."""
    get_ad_unit_hierarchy.main(client)

  def testGetMobileAdUnitSizes(self):
    """Test whether we can get mobile ad unit sizes."""
    get_mobile_ad_unit_sizes.main(client)

  def testGetTopLevelAdUnits(self):
    """Test whether we can get top level ad units."""
    get_top_level_ad_units.main(client)

  def testUpdateAdUnits(self):
    """Test whether we can update ad units."""
    update_ad_units.main(client, self.__class__.effective_root_ad_unit_id)

if __name__ == '__main__':
  if TEST_VERSION_V201208:
    unittest.main()
