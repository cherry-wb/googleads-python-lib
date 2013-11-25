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

"""This example displays country type names, codes, and whether the country
supports a secure server.

Tags: spotlight.getCountriesByCriteria
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


def main(client):
  # Initialize appropriate service.
  spotlight_service = client.GetSpotlightService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Set search criteria.
  country_search_criteria = {
      'secure': 'false'
  }

  # Get countries.
  results = spotlight_service.GetCountriesByCriteria(country_search_criteria)[0]

  # Display country names, codes and secure server support information.
  if results:
    for country in results:
      print ('Country with name \'%s\', country code \'%s\', and supports a'
             ' secure server? \'%s\'.'
             % (country['name'], country['countryCode'], country['secure']))
  else:
    print 'No countries found for your criteria.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client)
