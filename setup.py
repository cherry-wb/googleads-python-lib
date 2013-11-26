#!/usr/bin/python
#
# Copyright 2010 Google Inc.
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

"""Setup script for the Google Ads Python Client Library."""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import os
import sys

import warnings

warnings.filterwarnings(message='Can\'t import.*', action='ignore')

from adspygoogle import LIB_PYPI_AUTHOR
from adspygoogle import LIB_PYPI_AUTHOR_EMAIL
from adspygoogle import LIB_PYPI_NAME
from adspygoogle import LIB_PYPI_URL
from adspygoogle import LIB_PYPI_VERSION

from setuptools import setup

PACKAGES = ['adspygoogle', 'adspygoogle.common', 'adspygoogle.common.https',
            'adspygoogle.common.soappy', 'adspygoogle.adwords',
            'adspygoogle.adwords.util', 'adspygoogle.dfa', 'adspygoogle.dfp',
            'adspygoogle.SOAPpy', 'adspygoogle.SOAPpy.wstools',
            'adspygoogle.scripts.adspygoogle.adwords',
            'adspygoogle.scripts.adspygoogle.common',
            'adspygoogle.scripts.adspygoogle.dfa',
            'adspygoogle.scripts.adspygoogle.dfp']

PACKAGE_DATA = {'adspygoogle.adwords': [os.path.join('data', '*')],
                'adspygoogle.dfa': [os.path.join('data', '*')],
                'adspygoogle.dfp': [os.path.join('data', '*')]}

DEPENDENCIES = ['PyXML', 'ElementTree', 'cElementTree', 'Epydoc', 'fpconst',
                'mock', 'google-api-python-client', 'pytz']

# For manual installation, optionally remove PyXML and cElementTree for
# installation of adspygoogle on incompatible operating systems.
if '--no_PyXML' in sys.argv:
  print 'Not installing PyXML.'
  sys.argv.remove('--no_PyXML')
  DEPENDENCIES.remove('PyXML')

if '--no_cElementTree' in sys.argv:
  print 'Not installing cElementTree.'
  sys.argv.remove('--no_cElementTree')
  DEPENDENCIES.remove('cElementTree')

setup(name='adspygoogle',
      version=LIB_PYPI_VERSION,
      description=LIB_PYPI_NAME,
      author=LIB_PYPI_AUTHOR,
      author_email=LIB_PYPI_AUTHOR_EMAIL,
      maintainer=LIB_PYPI_AUTHOR,
      maintainer_email=LIB_PYPI_AUTHOR_EMAIL,
      url=LIB_PYPI_URL,
      license='Apache License 2.0',
      long_description=open('README.txt').read(),
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      platforms='any',
      keywords='adwords adxbuyer dfp dfa google',
      install_requires=DEPENDENCIES)
