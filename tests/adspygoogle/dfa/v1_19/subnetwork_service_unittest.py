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

"""Unit tests to cover SubnetworkService."""

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


class SubnetworkServiceTestV1_19(unittest.TestCase):

  """Unittest suite for SubnetworkService using v1_19."""

  SERVER = SERVER_V1_19
  VERSION = VERSION_V1_19
  client.debug = False
  test_super_user = False
  service = None
  user_self = None
  subnetwork_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSubnetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveSubnetwork(self):
    """Test whether we can save a subnetwork"""
    if self.__class__.test_super_user:
      network_id = self.__class__.user_self['networkId']
      subnetwork = {
          'name': 'Subnetwork #%s' % Utils.GetUniqueName(),
          'networkId': network_id,
      }
      subnetwork = self.__class__.service.SaveSubnetwork(subnetwork)
      self.__class__.subnetwork_id = subnetwork[0]['id']
      self.assert_(isinstance(subnetwork, tuple))

  def testGetSubnetwork(self):
    """Test whether we can fetch a subnetwork by id."""
    subnetwork_id = self.__class__.user_self['subnetworkId']
    self.assert_(isinstance(self.__class__.service.GetSubnetwork(
        subnetwork_id), tuple))

  def testGetSubnetworks(self):
    """Test whether we can fetch subnetworks by criteria."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworks(
        search_criteria), tuple))

  def testGetSubnetworkSummaries(self):
    """Test whether we can fetch subnetwork summaries."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworkSummaries(
        search_criteria), tuple))

  def testGetAllAvailablePermissions(self):
    """Test whether we can fetch all available permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllAvailablePermissions(), tuple))

  def testGetDefaultPermissions(self):
    """Test whether we can fetch default permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetDefaultPermissions(), tuple))


if __name__ == '__main__':
  unittest.main()
