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

"""Unit tests to cover CampaignService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import datetime
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa.v1_18 import client
from tests.adspygoogle.dfa.v1_18 import HTTP_PROXY
from tests.adspygoogle.dfa.v1_18 import SERVER_V1_18
from tests.adspygoogle.dfa.v1_18 import VERSION_V1_18


class CampaignServiceTestV1_18(unittest.TestCase):

  """Unittest suite for CampaignService using v1_18."""

  SERVER = SERVER_V1_18
  VERSION = VERSION_V1_18
  client.debug = False
  service = None
  campaign1 = None
  campaign2 = None
  advertiser_id = '0'
  landing_page_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testAddLandingPageToCampaign(self):
    """Test whether we can add a landing page to campaign."""
    if self.__class__.campaign1 is None:
      self.testSaveCampaign()
    landing_page = {
        'id': '-1',
        'url': 'http://www.example.com',
        'name': 'Landing page #%s' % Utils.GetUniqueName()
    }
    self.assert_(isinstance(self.__class__.service.AddLandingPageToCampaign(
        self.__class__.campaign1['id'], [landing_page]), tuple))

  def testCopyCampaigns(self):
    """Test whether we can copy campaigns."""
    if self.__class__.campaign1 is None:
      self.testSaveCampaign()
    requests = [{
        'campaignId': self.__class__.campaign1['id']
    }]
    self.assert_(isinstance(self.__class__.service.CopyCampaigns(requests),
                            tuple))

  def testDeleteCampaign(self):
    """Test whether we can delete a campaign."""
    if self.__class__.campaign2 is None:
      self.testSaveCampaign()
    self.assertEqual(self.__class__.service.DeleteCampaign(
        self.__class__.campaign2['id']), None)

  def testGetCampaign(self):
    """Test whether we can fetch a campaign."""
    if self.__class__.campaign1 is None:
      self.testSaveCampaign()
    self.assert_(isinstance(self.__class__.service.GetCampaign(
        self.__class__.campaign1['id']), tuple))

  def testGetCampaignsByCriteria(self):
    """Test whether we can fetch campaigns by criteria."""
    criteria = {
        'archiveFilter': {
            'inactiveOnly': 'true'
        }
    }
    self.assert_(isinstance(self.__class__.service.GetCampaignsByCriteria(
        criteria), tuple))

  def testGetLandingPagesForCampaign(self):
    """Test whether we can fetch landing pages for a campaign."""
    if self.__class__.campaign1 is None:
      self.testSaveCampaign()
    self.assert_(isinstance(self.__class__.service.GetLandingPagesForCampaign(
        self.__class__.campaign1['id']), tuple))

  def testSaveCampaign(self):
    """Test whether we can create a campaign."""
    self.testSaveLandingPage()
    dt = datetime.datetime.now()
    campaign = {
        'advertiserId': self.__class__.advertiser_id,
        'archived': 'false',
        'name': 'Campaign #%s' % Utils.GetUniqueName(),
        'defaultLandingPageId': self.__class__.landing_page_id,
        'endDate': '%s-01-31T12:00:00' % (dt.year + 1),
        'startDate': '%s-01-01T12:00:00' % (dt.year + 1),
        'creativeOptimizationConfiguration': {
            'minimumCreativeWeight': '5',
            'optimizationModelId': '1',
            'relativeStrength': '2'
        },
        'landingPageIds': [self.__class__.landing_page_id],
        'lookbackWindow': {
            'postClickEventLookbackWindow': '-1',
            'postImpressionEventLookbackWindow': '-1',
            'richMediaEventLookbackWindow': '-1'
        },
        'reachReportConfiguration': {
            'pageLevelFrequency': 'false',
            'siteLevelFrequency': 'false'
        }
    }
    campaign = self.__class__.service.SaveCampaign(campaign)
    self.__class__.campaign1 = campaign[0]
    self.assert_(isinstance(campaign, tuple))

    self.testSaveLandingPage()
    campaign = {
        'advertiserId': self.__class__.advertiser_id,
        'archived': 'false',
        'name': 'Campaign #%s' % Utils.GetUniqueName(),
        'defaultLandingPageId': self.__class__.landing_page_id,
        'endDate': '%s-01-31T12:00:00' % (dt.year + 1),
        'startDate': '%s-01-01T12:00:00' % (dt.year + 1),
        'creativeOptimizationConfiguration': {
            'minimumCreativeWeight': '5',
            'optimizationModelId': '1',
            'relativeStrength': '2'
        },
        'landingPageIds': [self.__class__.landing_page_id],
        'lookbackWindow': {
            'postClickEventLookbackWindow': '-1',
            'postImpressionEventLookbackWindow': '-1',
            'richMediaEventLookbackWindow': '-1'
        },
        'reachReportConfiguration': {
            'pageLevelFrequency': 'false',
            'siteLevelFrequency': 'false'
        }
    }
    campaign = self.__class__.service.SaveCampaign(campaign)
    self.__class__.campaign2 = campaign[0]
    self.assert_(isinstance(campaign, tuple))

  def testSaveLandingPage(self):
    """Test whether we can create a landing page."""
    landing_page = {
        'url': 'http://www.example.com',
        'name': 'Landing page #%s' % Utils.GetUniqueName()
    }
    landing_page = self.__class__.service.SaveLandingPage(landing_page)
    self.__class__.landing_page_id = landing_page[0]['id']
    self.assert_(isinstance(landing_page, tuple))


if __name__ == '__main__':
  unittest.main()
