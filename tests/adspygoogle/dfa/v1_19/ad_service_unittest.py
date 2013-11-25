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

"""Unit tests to cover AdService."""

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


class AdServiceTestV1_19(unittest.TestCase):

  """Unittest suite for AdService using v1_19."""

  SERVER = SERVER_V1_19
  VERSION = VERSION_V1_19
  client.debug = True
  service = None
  ad1 = None
  ad2 = None
  country_id = '0'
  campaign = None
  creative = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign is None:
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'pageSize': '10'
      }
      self.__class__.campaign = campaign_service.GetCampaignsByCriteria(
          search_criteria)[0]['records'][0]

    if self.__class__.creative is None:
      creative_service = client.GetCreativeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      creative_search_criteria = {
          'advertiserId': self.__class__.campaign['advertiserId']
      }
      self.__class__.creative = creative_service.GetCreatives(
          creative_search_criteria)[0]['records'][0]

  def testSaveAd(self):
    """Test whether we can create an ad."""
    campaign_id = self.__class__.campaign['id']
    start_date_before = self.__class__.campaign['startDate']
    end_date_before = self.__class__.campaign['endDate']
    start_date = str(int(start_date_before[0:4]) + 1) + start_date_before[4:]
    end_date = (str(int(end_date_before[0:4]) + 1) + end_date_before[4:8] +
                str(end_date_before[8:10]) + end_date_before[10:])
    ad = {
        'xsi_type': 'RotationGroup',
        'name': 'Ad #%s' % Utils.GetUniqueName(),
        'campaignId': campaign_id,
        'startTime': start_date,
        'endTime': end_date,
        'typeId': '1',
        'rotationType': '1',
        'id': '0',
        'active': 'false',
        'archived': 'false',
        'sizeId': self.__class__.creative['sizeId'],
        'priority': '1',
        'creativeAssignments': [{
            'active': 'True',
            'creativeId': self.__class__.creative['id'],
            'startDate': start_date,
            'endDate': end_date,
            'sequence': '1',
            'weight': '1',
            'clickThroughUrl': {
                'defaultLandingPageUsed': 'true'
            }
        }],
    }
    ad = self.__class__.service.SaveAd(ad)
    self.__class__.ad1 = ad[0]
    self.assert_(isinstance(ad, tuple))

    ad = {
        'xsi_type': 'DefaultAd',
        'name': 'Ad #%s' % Utils.GetUniqueName(),
        'campaignId': campaign_id,
        'startTime': start_date,
        'endTime': end_date,
        'typeId': '1',
        'id': '0',
        'active': 'false',
        'archived': 'false',
        'sizeId': self.__class__.creative['sizeId'],
        'creativeAssignment': {
            'active': 'True',
            'creativeId': self.__class__.creative['id'],
            'startDate': start_date,
            'endDate': end_date,
            'sequence': '1',
            'weight': '1',
            'clickThroughUrl': {
                'defaultLandingPageUsed': 'true'
            }
        }
    }
    ad = self.__class__.service.SaveAd(ad)
    self.__class__.ad2 = ad[0]
    self.assert_(isinstance(ad, tuple))

  def testCopyAds(self):
    """Test whether we can copy ads."""
    if self.__class__.ad1 is None:
      self.testSaveAd()
    ad_copy_request = {
        'adId':  self.__class__.ad1['id'],
        'campaignId': self.__class__.campaign['id']
    }
    self.assert_(isinstance(
        self.__class__.service.CopyAds([ad_copy_request]), tuple))

  def testDeleteAd(self):
    """Test whether we can delete an ad."""
    if self.__class__.ad2 is None:
      self.testSaveAd()
    self.assertEqual(self.__class__.service.DeleteAd(
        self.__class__.ad2['id']), None)

  def testGetAd(self):
    """Test whether we can get an ads."""
    if self.__class__.ad1 is None:
      self.testSaveAd()
    self.assert_(isinstance(
        self.__class__.service.GetAd(self.__class__.ad1['id']), tuple))

  def testGetAds(self):
    """Test whether we can fetch ads by criteria."""
    if self.__class__.ad1 is None:
      self.testSaveAd()
    ad_search_criteria = {
        'ids':  [self.__class__.ad1['id']]
    }
    self.assert_(isinstance(
        self.__class__.service.GetAds(ad_search_criteria), tuple))

  def testUpdateCreativeAssignmentProperties(self):
    """Test whether we can update creative assignment properties."""
    if self.__class__.ad1 is None:
      self.testSaveAd()
    creative_ad_association_update_request = {
        'adIds':  [self.__class__.ad1['id']],
        'creativeId': self.__class__.creative['id'],
        'clickThroughUrl': 'www.example.com',
        'propertiesToUpdate': ['clickThroughUrl']
    }
    self.assert_(isinstance(
        self.__class__.service.UpdateCreativeAssignmentProperties(
        creative_ad_association_update_request), tuple))

  def testGetAdTypes(self):
    """Test whether we can fetch ad types."""
    self.assert_(isinstance(self.__class__.service.GetAdTypes(),
                            tuple))

  def testGetAreaCodes(self):
    """Test whether we can fetch area codes."""
    if self.__class__.country_id == '0':
      self.testGetCountries()
    country_ids = [self.__class__.country_id]
    self.assert_(isinstance(self.__class__.service.GetAreaCodes(country_ids),
                            (tuple, type(None))))

  def testGetBandwidths(self):
    """Test whether we can fetch bandwidths."""
    self.assert_(isinstance(self.__class__.service.GetBandwidths(),
                            tuple))

  def testGetBroswers(self):
    """Test whether we can fetch browsers."""
    self.assert_(isinstance(self.__class__.service.GetBrowsers(),
                            tuple))

  def testGetCities(self):
    """Test whether we can fetch cities."""
    if self.__class__.country_id == '0':
      self.testGetCountries()
    city_search_criteria = {
        'countryIds':  [self.__class__.country_id]
    }
    self.assert_(isinstance(
        self.__class__.service.GetCities(city_search_criteria), tuple))

  def testGetCountries(self):
    """Test whether we can fetch countries."""
    countries = self.__class__.service.GetCountries()
    self.__class__.country_id = countries[0]['id']
    self.assert_(isinstance(countries, tuple))

  def testGetDesignatedMarketAreas(self):
    """Test whether we can fetch designated market areas."""
    self.assert_(isinstance(self.__class__.service.GetDesignatedMarketAreas(),
                            tuple))

  def testGetDomainNamesBySearchCriteria(self):
    """Test whether we can fetch domain names by search criteria."""
    domain_name_search_criteria = {
        'pageSize': '10'
    }
    self.assert_(isinstance(
        self.__class__.service.GetDomainNamesBySearchCriteria(
        domain_name_search_criteria), tuple))

  def testGetDomainTypes(self):
    """Test whether we can fetch domain types."""
    self.assert_(isinstance(self.__class__.service.GetDomainTypes(),
                            tuple))
  def testGetISPs(self):
    """Test whether we can fetch ISP types."""
    self.assert_(isinstance(self.__class__.service.GetISPs(),
                            tuple))

  def testGetMobilePlatforms(self):
    """Test whether we can fetch mobile platforms."""
    self.assert_(isinstance(self.__class__.service.GetMobilePlatforms(),
                            tuple))

  def testGetOSPs(self):
    """Test whether we can fetch OSP types."""
    self.assert_(isinstance(self.__class__.service.GetOSPs(),
                            tuple))

  def testGetOperatingSystems(self):
    """Test whether we can fetch operating systems."""
    self.assert_(isinstance(self.__class__.service.GetOperatingSystems(),
                            tuple))

  def testGetRegions(self):
    """Test whether we can fetch regions."""
    if self.__class__.country_id == '0':
      self.testGetCountries()
    country_ids = [self.__class__.country_id]
    self.assert_(isinstance(self.__class__.service.GetRegions(country_ids),
                            tuple))

  def testGetStates(self):
    """Test whether we can fetch states."""
    if self.__class__.country_id == '0':
      self.testGetCountries()
    country_ids = [self.__class__.country_id]
    self.assert_(isinstance(self.__class__.service.GetStates(country_ids),
                            tuple))

  def testGetUserListGroupsByCriteria(self):
    """Test whether we can fetch user list groups by criteria."""
    user_list_search_criteria = {}
    self.assert_(isinstance(
        self.__class__.service.GetUserListGroupsByCriteria(
        user_list_search_criteria), tuple))

  def testGetUserListsByCriteria(self):
    """Test whether we can fetch user lists by criteria."""
    user_list_search_criteria = {}
    self.assert_(isinstance(
        self.__class__.service.GetUserListsByCriteria(
        user_list_search_criteria), tuple))


if __name__ == '__main__':
  unittest.main()
