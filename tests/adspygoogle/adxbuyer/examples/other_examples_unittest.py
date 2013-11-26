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

"""Unit tests to cover other examples."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import time
import unittest

from examples.adspygoogle.adxbuyer.v201309.campaign_management import add_placements_in_bulk
from examples.adspygoogle.adxbuyer.v201309.error_handling import handle_partial_failures
from examples.adspygoogle.adxbuyer.v201309.optimization import get_placement_ideas
from tests.adspygoogle.adwords import client
from tests.adspygoogle.adwords import SERVER_V201309
from tests.adspygoogle.adwords import TEST_VERSION_V201309
from tests.adspygoogle.adwords import util
from tests.adspygoogle.adwords import VERSION_V201309


class OtherExamples(unittest.TestCase):

  """Unittest suite for other code examples."""

  SERVER = SERVER_V201309
  VERSION = VERSION_V201309
  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    time.sleep(1)
    client.use_mcc = False
    if not self.__class__.loaded:
      self.__class__.campaign_id = util.CreateTestRTBCampaign(
          client)
      self.__class__.ad_group_id = util.CreateTestCPMAdGroup(
          client, self.__class__.campaign_id)
      self.__class__.loaded = True

  def testAddPlacementsInBulk(self):
    """Tests whether we can add placements in bulk."""
    add_placements_in_bulk.main(client, self.__class__.ad_group_id)

  def testHandlePartialFailures(self):
    """Tests whether we can handle partial failures."""
    handle_partial_failures.main(client, self.__class__.ad_group_id)

  def testGetPlacementIdeas(self):
    """Tests whether we can get placement ideas."""
    get_placement_ideas.main(client)


if __name__ == '__main__':
  if TEST_VERSION_V201309:
    unittest.main()
