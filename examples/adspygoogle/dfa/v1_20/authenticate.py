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

"""This example authenticates using your DFA user name and password, and
displays the user profile token, DFA account name and ID.

This method of authentication is now discouraged in favor of using OAuth2. See
the example "use_oauth2.py".

Tags: login.authenticate
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


USERNAME = 'INSERT_USER_NAME_HERE'
PASSWORD = 'INSERT_PASSWORD_HERE'


def main(client, username, password):
  # Initialize appropriate service.
  login_service = client.GetLoginService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Authenticate.
  user_profile = login_service.Authenticate(username, password)[0]

  # Display user profile token, DFA account name and ID.
  print ('User profile token is \'%s\', DFA account name is \'%s\', and DFA'
         ' account ID is \'%s\'.' % (user_profile['token'],
                                     user_profile['networkName'],
                                     user_profile['networkId']))


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, USERNAME, PASSWORD)
