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

"""Unit tests to cover SpotlightService."""

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


class SpotlightServiceTestV1_18(unittest.TestCase):

  """Unittest suite for SpotlightService using v1_18."""

  SERVER = SERVER_V1_18
  VERSION = VERSION_V1_18
  client.debug = False
  test_super_user = False
  service = None
  activity_id = '0'
  activity_group_id = '0'
  configuration_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSpotlightService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testSaveSpotlightActivity(self):
    """Test whether we can save a spotlight activity."""
    if self.__class__.activity_group_id == '0':
      self.testSaveSpotlightActivityGroup()
    activity_group_id = self.__class__.activity_group_id
    spotlight_activity = {
        'name': 'SpotlightActivity #%s' % Utils.GetUniqueName(),
        'activityGroupId': activity_group_id,
        'activityTypeId': '1', # Counter Activity
        'tagMethodTypeId' : '1', # Standard
        'expectedUrl' : 'http://www.example.com',
        'countryId': '256' #USA
    }
    spotlight_activity = self.__class__.service.SaveSpotlightActivity(
        spotlight_activity)
    self.__class__.activity_id = spotlight_activity[0]['id']
    self.assert_(isinstance(spotlight_activity, tuple))

  def testDeleteSpotlightActivity(self):
    """Test whether we can delete a spotlight activity."""
    if self.__class__.test_super_user:
      if self.__class__.activity_id == '0':
        self.testSaveSpotlightActivity()
      self.assertEqual(self.__class__.service.DeleteSpotlightActivity(
          self.__class__.activity_id), None)
      self.__class__.activity_id = '0'

  def testGetSpotlightActivity(self):
    """Test whether we can fetch a spotlight activity by id."""
    if self.__class__.activity_id == '0':
      self.testSaveSpotlightActivity()
    activity_id = self.__class__.activity_id
    self.assert_(isinstance(self.__class__.service.GetSpotlightActivity(
        activity_id), tuple))

  def testGetSpotlightActivities(self):
    """Test whether we can fetch spotlight activities by criteria."""
    if self.__class__.activity_id == '0':
      self.testSaveSpotlightActivity()
    search_criteria = {
        'ids': [self.__class__.activity_id],
        'advertiserId': self.__class__.advertiser_id
    }
    self.assert_(isinstance(self.__class__.service.GetSpotlightActivities(
        search_criteria), tuple))

  def testGetSpotlightActivityTypes(self):
    """Test whether we can fetch spotlight activity types."""
    self.assert_(isinstance(
        self.__class__.service.GetSpotlightActivityTypes(), tuple))

  def testGetSpotlightTagCodeTypes(self):
    """Test whether we can fetch spotlight tag code types."""
    self.assert_(isinstance(
        self.__class__.service.GetSpotlightTagCodeTypes(), tuple))

  def testGetSpotlightTagFormatTypes(self):
    """Test whether we can fetch spotlight tag format types."""
    self.assert_(isinstance(
        self.__class__.service.GetSpotlightTagFormatTypes(), tuple))

  def testGetAvailableCustomSpotlightVariables(self):
    """Test whether we can fetch available custom spotlight variables."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableCustomSpotlightVariables(), tuple))

  def testGetAvailableStandardVariables(self):
    """Test whether we can fetch available standard spotlight variables."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableStandardVariables(), tuple))

  def testGetSpotlightTagMethodTypes(self):
    """Test whether we can fetch spotlight tag method types."""
    self.assert_(isinstance(
        self.__class__.service.GetSpotlightTagMethodTypes(), tuple))

  def testSaveSpotlightActivityGroup(self):
    """Test whether we can save a spotlight activity group."""
    if self.__class__.configuration_id == '0':
      self.testSaveSpotlightConfiguration()
    configuration_id = self.__class__.configuration_id
    spotlight_activity_group = {
        'name': 'SpotlightActivityGroup #%s' % Utils.GetUniqueName(),
        'groupType':  '1', # Counter Activity
        'spotlightConfigurationId': configuration_id
    }
    spotlight_activity_group = \
        self.__class__.service.SaveSpotlightActivityGroup(
            spotlight_activity_group)
    self.__class__.activity_group_id = spotlight_activity_group[0]['id']
    self.assert_(isinstance(spotlight_activity_group, tuple))

  def testDeleteSpotlightActivityGroup(self):
    """Test whether we can delete a spotlight activity group."""
    if self.__class__.test_super_user:
      if self.__class__.activity_group_id == '0':
        self.testSaveSpotlightActivityGroup()
      self.assertEqual(self.__class__.service.DeleteSpotlightActivityGroup(
          self.__class__.activity_group_id), None)
      self.__class__.activity_group_id = '0'

  def testGetSpotlightActivityGroups(self):
    """Test whether we can fetch spotlight activity group by criteria."""
    if self.__class__.test_super_user:
      if self.__class__.activity_group_id == '0':
        self.testSaveSpotlightActivityGroup()
      search_criteria = {
          'ids': [self.__class__.activity_group_id],
          'advertiserId' : self.__class__.advertiser_id
      }
      self.assert_(isinstance(self.__class__.service.GetSpotlightActivityGroups(
          search_criteria), tuple))

  def testSaveSpotlightConfiguration(self):
    """Test whether we can save a spotlight configuration."""
    spotlight_configuration = {
        'name': 'SpotlightConfiguration #%s' % Utils.GetUniqueName(),
        'id': self.__class__.advertiser_id,
        'firstDayOfWeek': '1',
        'motifEventsDays': '30',
        'clickDays': '30',
        'impressionDays': '30'
    }
    spotlight_configuration = self.__class__.service.SaveSpotlightConfiguration(
        spotlight_configuration)
    self.__class__.configuration_id = spotlight_configuration[0]['id']
    self.assert_(isinstance(spotlight_configuration, tuple))

  def testGetSpotlightConfiguration(self):
    """Test whether we can fetch a spotlight configuration by id."""
    if self.__class__.configuration_id == '0':
      self.testSaveSpotlightConfiguration()
    configuration_id = self.__class__.configuration_id
    self.assert_(isinstance(self.__class__.service.GetSpotlightConfiguration(
        configuration_id), tuple))

  def testGenerateTags(self):
    """Test whether we can generate tags for a spotlight activity."""
    if self.__class__.activity_id == '0':
      self.testSaveSpotlightActivity()
    self.assert_(isinstance(self.__class__.service.GenerateTags(
        [self.__class__.activity_id]), tuple))

  def testGetCountriesByCriteria(self):
    """Test whether we can fetch countries by criteria."""
    search_criteria = {
        'secure': 'true'
    }
    self.assert_(isinstance(self.__class__.service.GetCountriesByCriteria(
        search_criteria), tuple))


if __name__ == '__main__':
  unittest.main()
