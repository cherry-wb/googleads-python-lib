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

"""This code example creates a line item creative association for a creative
set.

To create creative sets, run create_creative_set.py. To create creatives, run
create_creatives.py. To determine which LICAs exist, run get_all_licas.py.

Tags: LineItemCreativeAssociationService.CreateLineItemCreativeAssociations
"""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient

CREATIVE_SET_ID = 'INSERT_CREATIVE_SET_ID_HERE'
LINE_ITEM_ID = 'INSERT_LINE_ITEM_ID_HERE'


def main(client, creative_set_id, line_item_id):
  # Initialize appropriate service.
  lica_service = client.GetService(
      'LineItemCreativeAssociationService', version='v201211')

  # Create LICA for a creative set.
  lica = {'creativeSetId': creative_set_id, 'lineItemId': line_item_id}

  # Add LICA.
  lica = lica_service.CreateLineItemCreativeAssociations([lica])[0]

  # Display results.
  print (('LICA with line item ID \'%s\' and creative set ID \'%s\' was '
          'created.') % (lica['lineItemId'], lica['creativeSetId']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CREATIVE_SET_ID, LINE_ITEM_ID)
