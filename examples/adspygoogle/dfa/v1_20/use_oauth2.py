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

"""This example demonstrates how to authenticate using OAuth2.

This example is intended for users who wish to use the oauth2client library
directly. Using a workflow similar to the example here, you can take advantage
of the oauth2client in a broader range of contexts than caching your refresh
token using the config.py scripts allows.

You can avoid having to use the oauth2client library directly by using the Ads
Python Client Library's config.py script to cache a client ID, client secret,
and refresh token for reuse.

This example is intended to be run from the command line as it takes user input.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import httplib2
import os
import sys

sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
from adspygoogle import DfaClient
from oauth2client.client import FlowExchangeError
from oauth2client.client import OAuth2WebServerFlow

DFA_USER_PROFILE_NAME = 'INSERT_DFA_USER_PROFILE_NAME_HERE'
# Visit https://code.google.com/apis/console to generate your client_id,
# client_secret and to register your redirect_uri.
# See the oauth2client wiki for more information on performing the OAuth2 flow:
# http://code.google.com/p/google-api-python-client/wiki/OAuth2
OAUTH2_CLIENT_ID = 'INSERT_OAUTH2_CLIENT_ID_HERE'
OAUTH2_CLIENT_SECRET = 'INSERT_OAUTH2_CLIENT_SECRET_HERE'


def main(user_profile_name, oauth2_client_id, oauth2_client_secret):
  # We're using the oauth2client library:
  # http://code.google.com/p/google-api-python-client/downloads/list
  flow = OAuth2WebServerFlow(
      client_id=oauth2_client_id,
      client_secret=oauth2_client_secret,
      scope='https://www.googleapis.com/auth/dfatrafficking',
      user_agent='oauth2 code example',
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  # Get the authorization URL to direct the user to.
  authorize_url = flow.step1_get_authorize_url()

  print ('Log in to your Google Account and open the following URL: \n%s\n' %
         authorize_url)
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  credential = None
  try:
    credential = flow.step2_exchange(code)
  except FlowExchangeError, e:
    sys.exit('Authentication has failed: %s' % e)

  # Create the DfpClient and set the OAuth2 credentials.
  client = DfaClient(headers={
      'Username': user_profile_name,
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

  advertiser_service = client.GetAdvertiserService(version='v1.20')

  advertiser_search_criteria = {
      'pageSize': '10'
  }

  # Get advertiser record set.
  results = advertiser_service.GetAdvertisers(advertiser_search_criteria)[0]

  # Display advertiser names, IDs and spotlight configuration IDs.
  if results['records']:
    for advertiser in results['records']:
      print ('Advertiser with name \'%s\', ID \'%s\', and spotlight '
             'configuration id \'%s\' was found.' %
             (advertiser['name'], advertiser['id'], advertiser['spotId']))
  else:
    print 'No advertisers found for your criteria.'

if __name__ == '__main__':
  main(DFA_USER_PROFILE_NAME, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)
