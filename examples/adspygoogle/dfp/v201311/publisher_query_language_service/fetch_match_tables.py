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

"""This example fetches data from PQL tables and creates match table files."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
import tempfile
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

# Initialize appropriate service.
pql_service = client.GetService(
    'PublisherQueryLanguageService', version='v201311')

line_items_file = tempfile.NamedTemporaryFile(prefix='line_items_',
                                              suffix='.csv',
                                              delete=False)
ad_units_file = tempfile.NamedTemporaryFile(prefix='ad_units_',
                                            suffix='.csv',
                                            delete=False)

line_items_pql_query = 'SELECT Name, Id, Status FROM Line_Item ORDER BY Id ASC'
ad_units_pql_query = 'SELECT Name, Id FROM Ad_Unit ORDER BY Id ASC'

# Downloads the response from PQL select statement to the specified file
print ('Saved line items to... %s' % DfpUtils.DownloadPqlResultSetToCsv(
    pql_service, line_items_pql_query, line_items_file).name)
print ('Saved ad units to... %s' % DfpUtils.DownloadPqlResultSetToCsv(
    pql_service, ad_units_pql_query, ad_units_file).name)
