#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Contains common constants for PyPI release scripts."""
__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import warnings
from adspygoogle.common import GenerateLibSig

try:
  from adspygoogle.adwords.AdWordsClient import AdWordsClient
except ImportError, e:
  warnings.warn('Can\'t import AdWordsClient: %s' % e)

try:
  from adspygoogle.dfa.DfaClient import DfaClient
except ImportError, e:
  warnings.warn('Can\'t import DfaClient: %s' % e)

try:
  from adspygoogle.dfp.DfpClient import DfpClient
except ImportError, e:
  warnings.warn('Can\'t import DfpClient: %s' % e)

LIB_PYPI_VERSION = '1.1.2'
LIB_PYPI_NAME = 'Google Ads Python Client Library'
LIB_PYPI_SHORT_NAME = 'adspygoogle'
LIB_PYPI_URL = 'http://code.google.com/p/google-api-ads-python'
LIB_PYPI_AUTHOR = 'Joseph DiLallo'
LIB_PYPI_AUTHOR_EMAIL = 'api.jdilallo@gmail.com'
LIB_PYPI_SIG = GenerateLibSig(LIB_PYPI_SHORT_NAME, LIB_PYPI_VERSION)
