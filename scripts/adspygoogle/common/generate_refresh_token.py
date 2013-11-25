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

"""This script generates a refresh token using OAuth 2.0.

This script is meant to be run from the command line and requires user input. It
will output a refresh token you can store and use for future requests.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import collections
import sys

from oauth2client import client


PRODUCT_TO_OAUTH_SCOPE = collections.OrderedDict([
    ('AdWords / Ad Exchange Buyer', 'https://adwords.google.com/api/adwords'),
    ('DoubleClick for Advertisers',
     'https://www.googleapis.com/auth/dfatrafficking'),
    ('DoubleClick for Publishers', 'https://www.google.com/apis/ads/publisher')
])


def ChooseProduct():
  """Prompt the user to choose which product they want a refresh token for.

  Returns:
    str The product the user chose. Will always be one of the keys from the
    PRODUCT_TO_OAUTH_SCOPE dictionary.
  """
  potential_products = PRODUCT_TO_OAUTH_SCOPE.keys()
  while True:
    print 'Please choose which product you want to use:'
    for index, product in enumerate(potential_products):
      print '\t%s) %s' % (index + 1, product)
    choice = raw_input('Please enter a number: ').strip()
    try:
      choice = int(choice) - 1
    except ValueError:
      print 'Invalid choice.'
      continue
    if 0 <= (choice) < len(potential_products):
      return potential_products[choice]
    print 'Invalid choice.'


def main():
  """Prompt the user for information to generate and output a refresh token."""
  print ('Please enter your OAuth 2.0 Client ID and Client Secret.\n'
         'These values can be generated from the Google APIs Console, '
         'https://code.google.com/apis/console under the API Access tab.\n'
         'Please use a Client ID for installed applications.')
  client_id = raw_input('Client ID: ').strip()
  client_secret = raw_input('Client Secret: ').strip()
  product = ChooseProduct()

  flow = client.OAuth2WebServerFlow(
      client_id=client_id,
      client_secret=client_secret,
      scope=PRODUCT_TO_OAUTH_SCOPE[product],
      user_agent='Ads Python Client Library',
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  authorize_url = flow.step1_get_authorize_url()

  print ('Log into the Google Account you use to access your %s account and go '
         'to the following URL: \n%s\n' % (product, authorize_url))
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  try:
    credential = flow.step2_exchange(code)
  except client.FlowExchangeError, e:
    print 'Authentication has failed: %s' % e
    sys.exit(1)
  else:
    print ('OAuth 2.0 authorization successful!\n\n'
           'Your refresh token is: %s' % credential.refresh_token)


if __name__ == '__main__':
  main()
