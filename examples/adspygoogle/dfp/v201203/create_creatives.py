#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""This code example creates new image creatives for a given advertiser. To
determine which companies are advertisers, run get_companies_by_filter.py.
To determine which creatives already exist, run get_all_creatives.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import base64
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
creative_service = client.GetService(
    'CreativeService', 'https://www.google.com', 'v201203')

# Set id of the advertiser (company) that all creatives will be assigned to.
advertiser_id = 'INSERT_ADVERTISER_COMPANY_ID_HERE'

# Create creative objects.
creatives = []
image_data = open(
    os.path.join('..', '..', '..', '..', 'tests', 'adspygoogle', 'dfp', 'data',
                 'medium_rectangle.jpg'), 'r').read()
image_data = base64.encodestring(image_data)

for i in xrange(5):
  creative = {
      'type': 'ImageCreative',
      'name': 'Image Creative #%s' % Utils.GetUniqueName(),
      'advertiserId': advertiser_id,
      'destinationUrl': 'http://google.com',
      'imageName': 'image.jpg',
      'imageByteArray': image_data,
      'size': {'width': '300', 'height': '250'}
  }
  creatives.append(creative)

# Add creatives.
creatives = creative_service.CreateCreatives(creatives)

# Display results.
for creative in creatives:
  print ('Image creative with id \'%s\', name \'%s\', and type \'%s\' was '
         'created and can be previewed at %s.'
         % (creative['id'], creative['name'], creative['Creative_Type'],
            creative['previewUrl']))
