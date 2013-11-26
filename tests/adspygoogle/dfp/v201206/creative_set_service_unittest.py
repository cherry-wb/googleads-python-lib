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

"""Unit tests to cover company service examples."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.dfp.v201206.creative_set_service import create_creative_set
from examples.adspygoogle.dfp.v201206.creative_set_service import get_all_creative_sets
from examples.adspygoogle.dfp.v201206.creative_set_service import get_creative_sets_by_statement
from examples.adspygoogle.dfp.v201206.creative_set_service import update_creative_set
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import SERVER_V201206
from tests.adspygoogle.dfp import TEST_VERSION_V201206
from tests.adspygoogle.dfp import util
from tests.adspygoogle.dfp import VERSION_V201206


class CreativeSetServiceTest(unittest.TestCase):
  """Unittest suite for CreativeSetService."""

  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.__class__.loaded:
      advertiser = util.CreateTestAdvertiser(client, SERVER_V201206,
                                             VERSION_V201206)
      self.__class__.test_master_creative_id = util.CreateTestCreative(
          client, SERVER_V201206, VERSION_V201206, advertiser)
      self.__class__.test_companion_creative_id = util.CreateTestCreative(
          client, SERVER_V201206, VERSION_V201206, advertiser)
      self.__class__.loaded = True

  def testCreateCreativeSets(self):
    """Test whether we can create creative sets."""
    create_creative_set.main(client, self.__class__.test_master_creative_id,
                             self.__class__.test_companion_creative_id)

  def testGetAllCreativeSets(self):
    """Test whether we can get all creative sets."""
    get_all_creative_sets.main(client)

  def testGetCreativeSetsByStatement(self):
    """Test whether we can get creative sets by statement."""
    get_creative_sets_by_statement.main(client,
                                        self.__class__.test_master_creative_id)

  def testUpdateCreativeSets(self):
    """Test whether we can update creative sets."""
    creative_set_id = util.CreateTestCreativeSet(
        client, SERVER_V201206, VERSION_V201206,
        self.__class__.test_master_creative_id,
        self.__class__.test_companion_creative_id)
    update_creative_set.main(client, creative_set_id,
                             self.__class__.test_companion_creative_id)

if __name__ == '__main__':
  if TEST_VERSION_V201206:
    unittest.main()
