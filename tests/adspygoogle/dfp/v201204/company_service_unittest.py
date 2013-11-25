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

"""Unit tests to cover company service examples."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.dfp.v201204.company_service import create_companies
from examples.adspygoogle.dfp.v201204.company_service import get_advertisers
from examples.adspygoogle.dfp.v201204.company_service import get_all_companies
from examples.adspygoogle.dfp.v201204.company_service import update_companies
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import SERVER_V201204
from tests.adspygoogle.dfp import TEST_VERSION_V201204
from tests.adspygoogle.dfp import util
from tests.adspygoogle.dfp import VERSION_V201204


class CompanyServiceTest(unittest.TestCase):
  """Unittest suite for CompanyService."""

  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.__class__.loaded:
      self.__class__.test_advertiser_id = util.CreateTestAdvertiser(
          client, SERVER_V201204, VERSION_V201204)
      self.__class__.loaded = True

  def testCreateCompany(self):
    """Test whether we can create a company."""
    create_companies.main(client)

  def testGetAdvertisers(self):
    """Test whether we can get all advertisers."""
    get_advertisers.main(client)

  def testGetAllCompanies(self):
    """Test whether we can fetch companies."""
    get_all_companies.main(client)

  def testUpdateCompanies(self):
    """Test whether we can update companies."""
    update_companies.main(
        client, self.__class__.test_advertiser_id)

if __name__ == '__main__':
  if TEST_VERSION_V201204:
    unittest.main()
