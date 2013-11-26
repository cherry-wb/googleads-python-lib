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

"""Unit tests to cover creative wrapper service examples."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.dfp.v201211.creative_wrapper_service import create_creative_wrappers
from examples.adspygoogle.dfp.v201211.creative_wrapper_service import deactivate_creative_wrapper
from examples.adspygoogle.dfp.v201211.creative_wrapper_service import get_active_creative_wrappers
from examples.adspygoogle.dfp.v201211.creative_wrapper_service import get_all_creative_wrappers
from examples.adspygoogle.dfp.v201211.creative_wrapper_service import update_creative_wrappers
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import SERVER_V201211
from tests.adspygoogle.dfp import TEST_VERSION_V201211
from tests.adspygoogle.dfp import util
from tests.adspygoogle.dfp import VERSION_V201211


class CreativeWrapperServiceTest(unittest.TestCase):
  """Unittest suite for CreativeWrapperService."""

  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.__class__.loaded:
      self.__class__.test_label_id = util.CreateTestLabel(
          client, SERVER_V201211, VERSION_V201211)
      self.__class__.test_creative_wrapper_id = util.CreateTestCreativeWrapper(
          client, SERVER_V201211, VERSION_V201211, self.__class__.test_label_id)
      self.__class__.loaded = True

  def testCreateCreativeWrappers(self):
    """Test whether we can create a creative wrapper."""
    create_creative_wrappers.main(client,
                                  util.CreateTestLabel(client, SERVER_V201211,
                                                       VERSION_V201211))

  def testGetAllCreativeWrappers(self):
    """Test whether we can get all creative wrappers."""
    get_all_creative_wrappers.main(client)

  def testUpdateCreativeWrappers(self):
    """Test whether we can update creative wrappers."""
    update_creative_wrappers.main(client,
                                  self.__class__.test_creative_wrapper_id)

  def testGetActiveCreativeWrappers(self):
    """Test whether we can get creative wrappers by statement."""
    get_active_creative_wrappers.main(client)

  def testDeactivateCreativeWrappers(self):
    """Test whether we can get perform an action on creative wrappers."""
    label_id = util.CreateTestLabel(client, SERVER_V201211, VERSION_V201211)
    util.CreateTestCreativeWrapper(client, SERVER_V201211, VERSION_V201211,
                                   label_id)
    deactivate_creative_wrapper.main(client, label_id)

if __name__ == '__main__':
  if TEST_VERSION_V201211:
    unittest.main()
