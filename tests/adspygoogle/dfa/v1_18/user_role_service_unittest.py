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

"""Unit tests to cover UserRoleService."""

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


class UserRoleServiceTestV1_18(unittest.TestCase):

  """Unittest suite for UserRoleService using v1_18."""

  SERVER = SERVER_V1_18
  VERSION = VERSION_V1_18
  client.debug = False
  service = None
  user_self = None
  user_role_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserRoleService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveUserRole(self):
    """Test whether we can save a user role"""
    subnetwork_id = self.__class__.user_self['subnetworkId']
    user_group_id = self.__class__.user_self['userGroupId']
    user_role = {
        'name': 'UserRole #%s' % Utils.GetUniqueName(),
        'subnetworkId': subnetwork_id,
        'parentUserRoleId': user_group_id,
        'permissions': [{'id': '2068'},{'id':'2037'}]
    }
    user_role = self.__class__.service.SaveUserRole(user_role)
    self.__class__.user_role_id = user_role[0]['id']
    self.assert_(isinstance(user_role, tuple))

  def testDeleteUserRole(self):
    """Test whether we can delete a user role."""
    if self.__class__.user_role_id == '0':
      self.testSaveUserRole()
    self.assertEqual(self.__class__.service.DeleteUserRole(
        self.__class__.user_role_id), None)
    self.__class__.user_role_id = '0'

  def testGetUserRole(self):
    """Test whether we can fetch a user role by id."""
    if self.__class__.user_role_id == '0':
      self.testSaveUserRole()
    user_role_id = self.__class__.user_role_id
    self.assert_(isinstance(self.__class__.service.GetUserRole(
        user_role_id), tuple))

  def testGetUserRoles(self):
    """Test whether we can fetch user roles by criteria."""
    if self.__class__.user_role_id == '0':
      self.testSaveUserRole()
    search_criteria = {
        'ids': [self.__class__.user_role_id]
    }
    self.assert_(isinstance(self.__class__.service.GetUserRoles(
        search_criteria), tuple))

  def testGetUserRoleSummaries(self):
    """Test whether we can fetch user role summaries."""
    if self.__class__.user_role_id == '0':
      self.testSaveUserRole()
    search_criteria = {
        'ids': [self.__class__.user_role_id]
    }
    self.assert_(isinstance(self.__class__.service.GetUserRoleSummaries(
        search_criteria), tuple))

  def testGetAvailablePermissions(self):
    """Test whether we can fetch available permissions."""
    subnetwork_id = self.__class__.user_self['subnetworkId']
    self.assert_(isinstance(
        self.__class__.service.GetAvailablePermissions(subnetwork_id), tuple))


if __name__ == '__main__':
  unittest.main()
