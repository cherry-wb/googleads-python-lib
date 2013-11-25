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

"""Unit tests to cover custom field service examples."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.dfp.v201211.custom_field_service import create_custom_field_options
from examples.adspygoogle.dfp.v201211.custom_field_service import create_custom_fields
from examples.adspygoogle.dfp.v201211.custom_field_service import deactivate_all_line_item_custom_fields
from examples.adspygoogle.dfp.v201211.custom_field_service import get_all_custom_fields
from examples.adspygoogle.dfp.v201211.custom_field_service import get_all_line_item_custom_fields
from examples.adspygoogle.dfp.v201211.custom_field_service import set_line_item_custom_field_value
from examples.adspygoogle.dfp.v201211.custom_field_service import update_custom_fields
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import SERVER_V201211
from tests.adspygoogle.dfp import TEST_VERSION_V201211
from tests.adspygoogle.dfp import util
from tests.adspygoogle.dfp import VERSION_V201211


class CustomFieldServiceTest(unittest.TestCase):
  """Unittest suite for CustomFieldService."""

  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.__class__.loaded:
      advertiser_id = util.CreateTestAdvertiser(
          client, SERVER_V201211, VERSION_V201211)
      trafficker_id = util.GetTrafficker(
          client, SERVER_V201211, VERSION_V201211)
      order_id = util.CreateTestOrder(
          client, SERVER_V201211, VERSION_V201211, advertiser_id, trafficker_id)
      ad_unit_id = util.CreateTestAdUnit(
          client, SERVER_V201211, VERSION_V201211)
      placement_id = util.CreateTestPlacement(
          client, SERVER_V201211, VERSION_V201211, [ad_unit_id])
      self.__class__.test_line_item_id = util.CreateTestLineItem(
          client, SERVER_V201211, VERSION_V201211, order_id, [placement_id])

      self.__class__.test_drop_down_custom_field_id = (
          util.CreateTestLineItemCustomField(
              client, SERVER_V201211, VERSION_V201211, 'DROP_DOWN'))

      self.__class__.loaded = True

  def testCreateCustomFields(self):
    """Test whether we can create custom fields."""
    create_custom_fields.main(client)

  def testCreateCustomFieldOptions(self):
    """Test whether we can create custom field options."""
    create_custom_field_options.main(
        client, self.__class__.test_drop_down_custom_field_id)

  def testDeactivateAllLineItemCustomFields(self):
    """Test deactivate all line item custom fields."""
    deactivate_all_line_item_custom_fields.main(client)

  def testGetAllCustomFields(self):
    """Test whether we can get all custom fields."""
    get_all_custom_fields.main(client)

  def testGetAllLineItemCustomFields(self):
    """Test whether we can get all line item custom fields."""
    get_all_line_item_custom_fields.main(client)

  def testSetLineItemCustomFieldValue(self):
    """Test whether we can set a value to a custom field on line item."""
    test_string_custom_field_id = util.CreateTestLineItemCustomField(
        client, SERVER_V201211, VERSION_V201211, 'STRING')
    test_drop_down_custom_field_id = util.CreateTestLineItemCustomField(
        client, SERVER_V201211, VERSION_V201211, 'DROP_DOWN')
    drop_down_custom_field_option_id = util.CreateTestLineItemCustomFieldOption(
        client, SERVER_V201211, VERSION_V201211, test_drop_down_custom_field_id)
    set_line_item_custom_field_value.main(
        client, test_string_custom_field_id,
        test_drop_down_custom_field_id,
        drop_down_custom_field_option_id,
        self.__class__.test_line_item_id)

  def testUpdateCustomFields(self):
    """Test whether we can update custom fields."""
    update_custom_fields.main(
        client, self.__class__.test_drop_down_custom_field_id)

if __name__ == '__main__':
  if TEST_VERSION_V201211:
    unittest.main()
