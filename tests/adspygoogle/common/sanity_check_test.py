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

"""Unit tests to cover SanityCheck."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.common import SanityCheck
from adspygoogle.common.Errors import ValidationError


class SanityCheckTest(unittest.TestCase):

  """Tests for the adspygoogle.common.SanityCheck module."""

  def testValidateConfigXmlParser_PyXML(self):
    """Tests the ValidateConfigXmlParser function accepts PyXML's values."""
    SanityCheck.ValidateConfigXmlParser('1')
    SanityCheck.ValidateConfigXmlParser(u'1')

  def testValidateConfigXmlParser_ETree(self):
    """Tests the ValidateConfigXmlParser function accepts ETree's values."""
    SanityCheck.ValidateConfigXmlParser('2')
    SanityCheck.ValidateConfigXmlParser(u'2')

  def testValidateConfigXmlParser_invalid(self):
    """Tests the ValidateConfigXmlParser function."""
    self.assertRaises(ValidationError, SanityCheck.ValidateConfigXmlParser, '3')
    self.assertRaises(ValidationError, SanityCheck.ValidateConfigXmlParser, 1)
    self.assertRaises(ValidationError, SanityCheck.ValidateConfigXmlParser,
                      'False')


if __name__ == '__main__':
  unittest.main()
