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

"""This example demonstrates how to authenticate using OAuth2.

This example is meant to be run from the command line and requires
user input.
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import httplib2
import os
import sys

sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
from adspygoogle import DfpClient
from oauth2client.client import FlowExchangeError
from oauth2client.client import OAuth2WebServerFlow

APPLICATION_NAME = 'INSERT_APPLICATION_NAME_HERE'
NETWORK_CODE = 'INSERT_NETWORK_CODE_HERE'
# Visit https://code.google.com/apis/console to generate your client_id,
# client_secret and to register your redirect_uri.
# See the oauth2client wiki for more information on performing the OAuth2 flow:
# http://code.google.com/p/google-api-python-client/wiki/OAuth2
OAUTH2_CLIENT_ID = 'INSERT_OAUTH2_CLIENT_ID_HERE'
OAUTH2_CLIENT_SECRET = 'INSERT_OAUTH2_CLIENT_SECRET_HERE'


def main(application_name, network_code, oauth2_client_id,
         oauth2_client_secret):
  # We're using the oauth2client library:
  # http://code.google.com/p/google-api-python-client/downloads/list
  flow = OAuth2WebServerFlow(
      client_id=oauth2_client_id,
      client_secret=oauth2_client_secret,
      scope='https://www.google.com/apis/ads/publisher',
      user_agent='oauth2 code example')

  # Get the authorization URL to direct the user to.
  authorize_url = flow.step1_get_authorize_url()

  print ('Log in to your DFP account and open the following URL: \n%s\n' %
         authorize_url)
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  credential = None
  try:
    credential = flow.step2_exchange(code)
  except FlowExchangeError, e:
    sys.exit('Authentication has failed: %s' % e)

  # Create the DfpClient and set the OAuth2 credentials.
  client = DfpClient(headers={
      'networkCode': network_code,
      'applicationName': application_name,
      'userAgent': 'OAuth2 Example',
      'oauth2credentials': credential
  })

  # OAuth2 credentials objects can be reused
  credentials = client.oauth2credentials
  print 'OAuth2 authorization successful!'

  # OAuth2 credential objects can be refreshed via credentials.refresh() - the
  # access token expires after 1 hour.
  credentials.refresh(httplib2.Http())

  # Note: you could simply set the credentials as below and skip the previous
  # steps once access has been granted.
  client.oauth2credentials = credentials

  network_service = client.GetService('NetworkService', version='v201208')

  # Get all networks that you have access to with the current login credentials.
  networks = network_service.GetAllNetworks()

  for network in networks:
    print ('Network with network code \'%s\' and display name \'%s\' was found.'
           % (network['networkCode'], network['displayName']))

  print
  print 'Number of results found: %s' % len(networks)

if __name__ == '__main__':
  main(APPLICATION_NAME, NETWORK_CODE, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)
