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

"""Unit tests to cover ChangeLogService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from tests.adspygoogle.dfa.v1_18 import client
from tests.adspygoogle.dfa.v1_18 import HTTP_PROXY
from tests.adspygoogle.dfa.v1_18 import SERVER_V1_18
from tests.adspygoogle.dfa.v1_18 import VERSION_V1_18


class ChangeLogServiceTestV1_18(unittest.TestCase):

  """Unittest suite for ChangeLogService using v1_18."""

  SERVER = SERVER_V1_18
  VERSION = VERSION_V1_18
  client.debug = False
  service = None
  advertiser_id = '0'
  change_log_record_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetChangeLogService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    search_criteria = {}
    self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
        search_criteria)[0]['records'][0]['id']

  def testGetChangeLogObjectTypes(self):
    """Test whether we can fetch object types that support change logs."""
    self.assert_(isinstance(self.__class__.service.GetChangeLogObjectTypes(),
                            tuple))

  def testGetChangeLogRecord(self):
    """Test whether we can fetch a change log record."""
    if self.__class__.change_log_record_id == '0':
      self.testGetChangeLogRecords()
    change_log_record_id = self.__class__.change_log_record_id
    self.assert_(isinstance(self.__class__.service.GetChangeLogRecord(
        change_log_record_id), tuple))

  def testGetChangeLogRecordForObjectType(self):
    """Test whether we can fetch change log record for given id and object type.
    """
    if self.__class__.change_log_record_id == '0':
      self.testGetChangeLogRecords()
    change_log_record_id = self.__class__.change_log_record_id
    object_type_id = '1'
    self.assert_(isinstance(
        self.__class__.service.GetChangeLogRecordForObjectType(
            change_log_record_id, object_type_id), tuple))

  def testGetChangeLogRecords(self):
    """Test whether we can fetch change log records."""
    criteria = {
        'objectId': self.__class__.advertiser_id
    }
    records = self.__class__.service.GetChangeLogRecords(criteria)
    self.__class__.change_log_record_id = records[0]['records'][0]['id']
    self.assert_(isinstance(records, tuple))

  def testUpdateChangeLogRecordComments(self):
    """Test whether we can update change log record comments."""
    if self.__class__.change_log_record_id == '0':
      self.testGetChangeLogRecords()
    change_log_record_id = self.__class__.change_log_record_id
    comments = 'This is a cool change!'
    self.assertEqual(self.__class__.service.UpdateChangeLogRecordComments(
        change_log_record_id, comments), None)

  def testUpdateChangeLogRecordCommentsForObjectType(self):
    """Test whether we can update change log record comments for object type."""
    if self.__class__.change_log_record_id == '0':
      self.testGetChangeLogRecords()
    change_log_record_id = self.__class__.change_log_record_id
    comments = 'This is a very cool change!'
    object_type_id = '1'
    self.assertEqual(
        self.__class__.service.UpdateChangeLogRecordCommentsForObjectType(
            change_log_record_id, comments, object_type_id), None)


if __name__ == '__main__':
  unittest.main()
