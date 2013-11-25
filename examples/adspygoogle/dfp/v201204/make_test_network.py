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

"""This example creates a test network.

You do not need to have a DFP account to
run this example, but you do need to have a new Google account (created at
http://www.google.com/accounts/newaccount) that is not associated with any
other DFP networks (including old sandbox networks). Once this network is
created, you can supply the network code in your settings to make calls to
other services.

Please see the following URL for more information:
https://developers.google.com/doubleclick-publishers/docs/signup
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
network_service = client.GetService('NetworkService', version='v201204')

# Get the current network.
network = network_service.MakeTestNetwork()[0]

# Display results.
print ('Test network with network code \'%s\' and display name \'%s\' created.'
       % (network['networkCode'], network['displayName']))
print ('You may now sign in at http://www.google.com/dfp/main?networkCode=%s' %
       network['networkCode'])
