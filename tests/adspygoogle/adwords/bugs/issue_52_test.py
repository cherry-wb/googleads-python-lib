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

"""Test to cover issue 52.

Ensures that ReportDownloader throws a useful error when urllib2.urlopen raises
a urllib2.URLError.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
import urllib2
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock

from adspygoogle import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsError


class Issue52Test(unittest.TestCase):
  """Tests for Issue 52."""

  def setUp(self):
    """Prepare unittest."""
    client = AdWordsClient(headers={'authToken': ' ',
                                    'userAgent': ' ',
                                    'developerToken': ' '})
    self.service = client.GetReportDownloader()

  def testHandleUrlError(self):
    """Tests that ReportDownloader handles a URLError properly."""
    reason = 'Socket exception!'
    adwords_report_response = urllib2.URLError(reason)

    def RaiseMyError(*unused_args):
      raise adwords_report_response

    urllib2.urlopen = mock.Mock(side_effect=RaiseMyError)

    try:
      self.service._ReportDownloader__MakeRequest('url', payload='nothing')
    except AdWordsError, e:
      self.assertTrue(reason in str(e))


if __name__ == '__main__':
  unittest.main()
