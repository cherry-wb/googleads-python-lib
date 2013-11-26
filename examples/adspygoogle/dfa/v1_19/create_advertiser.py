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

"""This example creates an advertiser in a given DFA network. To get the network
ID, run authenticate.py.

Tags: advertiser.saveAdvertiser
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient
from adspygoogle.common import Utils


def main(client):
  # Initialize appropriate service.
  advertiser_service = client.GetAdvertiserService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Construct and save advertiser.
  advertiser = {
      'name': 'Advertiser %s' % Utils.GetUniqueName(),
      'approved': 'true'
  }

  result = advertiser_service.SaveAdvertiser(advertiser)[0]

  # Display results.
  if result:
    print 'Advertiser with ID \'%s\' was created.' % result['id']
  else:
    print 'No advertiser was created.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
