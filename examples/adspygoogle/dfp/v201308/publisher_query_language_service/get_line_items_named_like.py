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

"""This example gets all line items with names starting with 'line item'."""

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
    'PublisherQueryLanguageService', version='v201308')

output_file = tempfile.NamedTemporaryFile(prefix='line_items_named_like_',
                                          suffix='.csv',
                                          delete=False)

# Create bind value to select line items with names starting with 'line item'.
values = [{
    'key': 'name',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'line item%'
    }
}]

pql_query = ('SELECT Name, Id, Status FROM Line_Item '
             'WHERE Name LIKE :name')

# Downloads the response from PQL select statement to the specified file
print ('Saved line items to... %s' % DfpUtils.DownloadPqlResultSetToCsv(
    pql_service, pql_query, output_file, values).name)
