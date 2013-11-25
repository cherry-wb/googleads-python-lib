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

"""This code example gets a forecast for an existing line item. To determine
which ine items exist, run get_all_line_items.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

# Initialize appropriate service.
forecast_service = client.GetService('ForecastService', version='v201308')

# Set the line item to get a forecast for.
line_item_id = 'INSERT_LINE_ITEM_ID'

# Get forecast for line item.
forecast = forecast_service.GetForecastById(line_item_id)[0]
matched = long(forecast['matchedUnits'])
available_percent = (((long(forecast['availableUnits'])/(matched * 1.0)) * 100)
                     if matched != 0 else 0)
contending_line_items = ([] if 'contendingLineItems' not in forecast
                         else forecast['contendingLineItems'])

# Display results.
print '%s %s matched.' % (matched, forecast['unitType'].lower())
print '%s%% %s available.' % (available_percent, forecast['unitType'].lower())
print '%d contending line items.' % len(contending_line_items)

if 'possibleUnits' in forecast:
  possible_percent = (long(forecast['possibleUnits'])/(matched * 1.0)) * 100
  print '%s%% %s possible' % (possible_percent, forecast['unitType'].lower())
  