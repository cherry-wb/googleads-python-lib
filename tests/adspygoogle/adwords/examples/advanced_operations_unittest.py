#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""Unit tests to cover Advanced Operations examples."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.adwords.v201309.advanced_operations import add_ad_group_bid_modifier
from examples.adspygoogle.adwords.v201309.advanced_operations import add_click_to_download_ad
from examples.adspygoogle.adwords.v201309.advanced_operations import add_site_links
from examples.adspygoogle.adwords.v201309.advanced_operations import create_and_attach_shared_keyword_set
from examples.adspygoogle.adwords.v201309.advanced_operations import create_shared_bidding_strategies
from examples.adspygoogle.adwords.v201309.advanced_operations import find_and_remove_criteria_from_shared_set
from examples.adspygoogle.adwords.v201309.advanced_operations import get_ad_group_bid_modifier
from tests.adspygoogle.adwords import client
from tests.adspygoogle.adwords import util
from tests.adspygoogle.adwords import SERVER_V201309
from tests.adspygoogle.adwords import TEST_VERSION_V201309
from tests.adspygoogle.adwords import VERSION_V201309


class AdvancedOperations(unittest.TestCase):

  """Unittest suite for Advanced Operations code examples."""

  SERVER = SERVER_V201309
  VERSION = VERSION_V201309
  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.loaded:
      self.campaign_id = util.CreateTestCampaign(client)
      self.ad_group_id = util.CreateTestAdGroup(client, self.campaign_id)

  def testAddClickToDownloadAd(self):
    """Tests whether we can create an account."""
    add_click_to_download_ad.main(client, self.ad_group_id)

  def testAddSiteLink(self):
    """Test whether we can get account alerts."""
    add_site_links.main(client, self.campaign_id)

  def testAddAndRemoveSharedCriteria(self):
    """Tests whether we can create, attach, and remove a shared keyword set."""
    create_and_attach_shared_keyword_set.main(client, self.campaign_id)
    find_and_remove_criteria_from_shared_set.main(client, self.campaign_id)

  def testAddAndRetrieveAdGroupBidModifier(self):
    add_ad_group_bid_modifier.main(client, self.ad_group_id, '1.5')
    get_ad_group_bid_modifier.main(client)

  def testCreateSharedBiddingStrategies(self):
    create_shared_bidding_strategies.main(client, None)


if __name__ == '__main__':
  if TEST_VERSION_V201309:
    unittest.main()
