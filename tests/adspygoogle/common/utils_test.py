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

"""Unit tests to cover Utils."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.common import Utils


# Location of a cached 502 to parse.
BUFFER_FILE_LOCATION = os.path.join('data', 'http_error_502.html')
TEST_502 = open(BUFFER_FILE_LOCATION).read()


class UtilsTest(unittest.TestCase):

  """Tests for the adspygoogle.common.Utils module."""

  def testBoolTypeConvert_toBool_true(self):
    """Tests the BoolTypeConvert function accepts True values."""
    self.assertEqual(True, Utils.BoolTypeConvert(True))
    self.assertEqual(True, Utils.BoolTypeConvert('1'))
    self.assertEqual(True, Utils.BoolTypeConvert('y'))
    self.assertEqual(True, Utils.BoolTypeConvert('Y'))
    self.assertEqual(True, Utils.BoolTypeConvert('yes'))
    self.assertEqual(True, Utils.BoolTypeConvert('Yes'))
    self.assertEqual(True, Utils.BoolTypeConvert('t'))
    self.assertEqual(True, Utils.BoolTypeConvert('true'))
    self.assertEqual(True, Utils.BoolTypeConvert('TRUE'))
    self.assertEqual(True, Utils.BoolTypeConvert(1))
    self.assertEqual(True, Utils.BoolTypeConvert(u'1'))
    self.assertEqual(True, Utils.BoolTypeConvert(u'y'))
    self.assertEqual(True, Utils.BoolTypeConvert(u'Y'))
    self.assertEqual(True, Utils.BoolTypeConvert(u'yes'))
    self.assertEqual(True, Utils.BoolTypeConvert(u'Yes'))
    self.assertEqual(True, Utils.BoolTypeConvert(u't'))
    self.assertEqual(True, Utils.BoolTypeConvert(u'true'))
    self.assertEqual(True, Utils.BoolTypeConvert(u'TRUE'))

  def testBoolTypeConvert_toBool_false(self):
    """Tests the BoolTypeConvert function accepts False values."""
    self.assertEqual(False, Utils.BoolTypeConvert(False))
    self.assertEqual(False, Utils.BoolTypeConvert('0'))
    self.assertEqual(False, Utils.BoolTypeConvert('n'))
    self.assertEqual(False, Utils.BoolTypeConvert('N'))
    self.assertEqual(False, Utils.BoolTypeConvert('no'))
    self.assertEqual(False, Utils.BoolTypeConvert('No'))
    self.assertEqual(False, Utils.BoolTypeConvert('f'))
    self.assertEqual(False, Utils.BoolTypeConvert('false'))
    self.assertEqual(False, Utils.BoolTypeConvert('False'))
    self.assertEqual(False, Utils.BoolTypeConvert(0))
    self.assertEqual(False, Utils.BoolTypeConvert(u'0'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'n'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'N'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'no'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'No'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'f'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'false'))
    self.assertEqual(False, Utils.BoolTypeConvert(u'FALSE'))

  def testBoolTypeConvert_toBool_invalid(self):
    """Tests the BoolTypeConvert function."""
    self.assertRaises(LookupError, Utils.BoolTypeConvert, '3')
    self.assertRaises(LookupError, Utils.BoolTypeConvert, u'Yessum')

  def testGetErrorFromHtml(self):
    """Test whether we can handle and report 502 errors."""
    trigger_msg = ('502 Server Error. The server encountered a temporary error'
                   ' and could not complete yourrequest. Please try again in 30'
                   ' seconds.')

    self.assertEqual(trigger_msg, Utils.GetErrorFromHtml(TEST_502))


if __name__ == '__main__':
  unittest.main()
