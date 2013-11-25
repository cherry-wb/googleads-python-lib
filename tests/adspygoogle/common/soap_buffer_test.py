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

"""Unit tests to cover SoapBuffer."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.common.SoapBuffer import SoapBuffer


# Location of a cached buffer to parse.
BUFFER_FILE_LOCATION = os.path.join('data', 'soap_buffer.txt')
TEST_BUFFER = open(BUFFER_FILE_LOCATION).read()


class SoapBufferTest(unittest.TestCase):

  """Tests for the adspygoogle.common.SoapBuffer module."""

  def testGetFaultAsDict_PyXML_PrettyOff(self):
    """Tests the GetFaultAsDict function."""
    self._RunGetFaultAsDict(SoapBuffer('1', False))

  def testGetFaultAsDict_PyXML_PrettyOn(self):
    """Tests the GetFaultAsDict function."""
    self._RunGetFaultAsDict(SoapBuffer('1', True))

  def testGetFaultAsDict_ETree_PrettyOff(self):
    """Tests the GetFaultAsDict function."""
    self._RunGetFaultAsDict(SoapBuffer('2', False))

  def testGetFaultAsDict_ETree_PrettyOn(self):
    """Tests the GetFaultAsDict function."""
    self._RunGetFaultAsDict(SoapBuffer('2', True))

  def _RunGetFaultAsDict(self, buffer_):
    """Tests the GetFaultAsDict function."""
    buffer_.write(TEST_BUFFER)

    expected_output = {
        'faultcode': 'soap:Server',
        'detail': {
            'type': 'ApiException',
            'errors': [{
                'externalPolicyDescription': ('Please correct the '
                                              'capitalization in the following '
                                              'phrase(s): '
                                              '\'AAAAAAAAAAAAAAAAAAAAA\''),
                'trigger': None,
                'key': {
                    'violatingText': 'AAAAAAAAAAAAAAAAAAAAA',
                    'policyName': 'capitalization'
                },
                'errorString': 'PolicyViolationError.POLICY_ERROR',
                'violatingParts': {
                    'index': '0',
                    'length': '21'
                },
                'type': 'PolicyViolationError',
                'isExemptable': 'true',
                'externalPolicyName': ('[Capitalization] Excessive '
                                       'capitalization'),
                'externalPolicyUrl': None,
                'fieldPath': 'operations[0].operand.ad.headline'
            }],
            'message': ('[AdPolicyError{super=PolicyViolationError.POLICY_ERROR'
                        ' @ operations[0].operand.ad.headline, '
                        'key=PolicyViolationKey{policyName=capitalization,'
                        'violatingText=AAAAAAAAAAAAAAAAAAAAA}, '
                        'externalPolicyName=[Capitalization] Excessive '
                        'capitalization, externalPolicyUrl=, '
                        'externalPolicyDescription=Please correct the '
                        'capitalization in the following phrase(s): '
                        '\'AAAAAAAAAAAAAAAAAAAAA\', isExemtable=true, '
                        'violatingParts=[Part{index=0, length=21}]}]]')
        },
        'faultstring': ('[AdPolicyError{super=PolicyViolationError.POLICY_ERROR'
                        ' @ operations[0].operand.ad.headline, '
                        'key=PolicyViolationKey{policyName=capitalization,'
                        'violatingText=AAAAAAAAAAAAAAAAAAAAA}, '
                        'externalPolicyName=[Capitalization] Excessive '
                        'capitalization, externalPolicyUrl=, '
                        'externalPolicyDescription=Please correct the '
                        'capitalization in the following phrase(s): '
                        '\'AAAAAAAAAAAAAAAAAAAAA\', isExemtable=true, '
                        'violatingParts=[Part{index=0, length=21}]}]]')
    }

    self.assertEqual(expected_output, buffer_.GetFaultAsDict())


if __name__ == '__main__':
  unittest.main()
