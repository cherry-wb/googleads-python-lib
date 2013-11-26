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

"""This example gets geographic criteria from the Geo_Target table.

   The types available to filter on include 'City', 'Country', 'Region',
   'State', 'Postal_Code', and 'DMA_Region' (i.e. Metro).

   A full list of available geo target types can be found at
   https://developers.google.com/doubleclick-publishers/docs/reference/v201308/PublisherQueryLanguageService
"""

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

output_file = tempfile.NamedTemporaryFile(prefix='geo_target_type_',
                                          suffix='.csv',
                                          delete=False)

# Create bind value to select geo-targets of type 'City'.
values = [{
    'key': 'type',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'City'
    }
}]

pql_query = ('SELECT Name, Id FROM Geo_Target '
             'WHERE targetable = true AND Type = :type')

# Downloads the response from PQL select statement to the specified file
print ('Saved geo targets to... %s' % DfpUtils.DownloadPqlResultSetToCsv(
    pql_service, pql_query, output_file, values).name)
