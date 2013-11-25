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

"""Unit tests to cover Basic Operations examples."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
import time
import unittest
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

from examples.adspygoogle.adxbuyer.v201309.basic_operations import add_ad_groups
from examples.adspygoogle.adxbuyer.v201309.basic_operations import add_campaigns
from examples.adspygoogle.adxbuyer.v201309.basic_operations import add_placements
from examples.adspygoogle.adxbuyer.v201309.basic_operations import add_third_party_redirect_ad
from examples.adspygoogle.adxbuyer.v201309.basic_operations import delete_placement
from examples.adspygoogle.adxbuyer.v201309.basic_operations import get_placements
from examples.adspygoogle.adxbuyer.v201309.basic_operations import get_third_party_redirect_ads
from examples.adspygoogle.adxbuyer.v201309.basic_operations import update_placement
from tests.adspygoogle.adwords import client
from tests.adspygoogle.adwords import SERVER_V201309
from tests.adspygoogle.adwords import TEST_VERSION_V201309
from tests.adspygoogle.adwords import util
from tests.adspygoogle.adwords import VERSION_V201309


class BasicOperations(unittest.TestCase):

  """Unittest suite for Account Management code examples."""

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
      self.__class__.placement_id = util.CreateTestPlacement(
          client, self.__class__.ad_group_id)
      self.__class__.loaded = True

  def testAddAdGroups(self):
    """Tests whether we can add ad groups."""
    add_ad_groups.main(client, self.__class__.campaign_id)

  def testAddCampaigns(self):
    """Tests whether we can add campaigns."""
    add_campaigns.main(client)

  def testAddPlacements(self):
    """Tests whether we can add placements."""
    add_placements.main(client, self.__class__.ad_group_id)

# TODO(user): currently we get an error trying to set impressionBeaconUrl in
# sandbox
  def testAddThirdPartyRedirectAd(self):
    """Tests whether we can add a third party redirect ad."""
    add_third_party_redirect_ad.main(client, self.__class__.ad_group_id)

  def testGetPlacements(self):
    """Tests whether we can get placements."""
    get_placements.main(client)

  def testGetThirdpartyRedirectAds(self):
    """Tests whether we can get third party redirect ads."""
    get_third_party_redirect_ads.main(client, self.__class__.ad_group_id)

  def testUpdatePlacement(self):
    """Tests whether we can update a placement."""
    update_placement.main(client, self.__class__.ad_group_id,
                          self.__class__.placement_id)

  def testZDeletePlacement(self):
    """Tests whether we can delete a placement."""
    delete_placement.main(client, self.__class__.ad_group_id,
                          self.__class__.placement_id)

if __name__ == '__main__':
  if TEST_VERSION_V201309:
    unittest.main()
