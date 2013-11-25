#!/usr/bin/python
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

"""Settings and configurations for the client library."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle
import sys

from adspygoogle.common import GenerateLibSig
from adspygoogle.common import Utils
from adspygoogle.common import VERSION
from adspygoogle.common.Errors import MissingPackageError


LIB_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LIB_NAME = 'DoubleClick for Advertisers API Python Client Library'
LIB_SHORT_NAME = 'DfaApi-Python'
LIB_URL = 'http://code.google.com/p/google-api-ads-python/'
LIB_AUTHOR = 'Joseph DiLallo'
LIB_AUTHOR_EMAIL = 'api.jdilallo@gmail.com'
LIB_VERSION = '2.4.1'
LIB_MIN_COMMON_VERSION = '3.1.0'
LIB_SIG = GenerateLibSig(LIB_SHORT_NAME, LIB_VERSION)

if VERSION < LIB_MIN_COMMON_VERSION:
  msg = ('Unsupported version of the core module is detected. Please download '
         'the latest version of client library at %s.' % LIB_URL)
  raise MissingPackageError(msg)

# Tuple of strings representing API versions.
API_VERSIONS = ('v1.19', 'v1.20')
DEFAULT_API_VERSION = API_VERSIONS[-1]

# Accepted combinations of headers which user has to provide. Either one of
# these is required in order to make a succesful API request.
REQUIRED_SOAP_HEADERS = (('Username', 'Password'),
                         ('Username', 'AuthToken'),
                         ('Username', 'oauth2credentials'))

WSSE_NS = ('http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-'
           'secext-1.0.xsd')
