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

"""This example replaces an In-Stream asset in an existing In-Stream video
creative with a new In-Stream asset. To create an In-Stream video creative,
run create_in_stream_video_creative.py. To add an In-Stream asset to an
In-Stream video creative, run upload_in_stream_asset.py.

This example replaces a companion ad asset in the target creative because the
'companion' flag on the InStreamAssetUploadRequest was set to 'true'. You can
use the same workflow to replace a non-linear ad by setting the 'nonLinear' flag
instead. You may not use this method to swap out media files (a.k.a. video
assets).

Tags: creative.replaceInStreamAsset
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import base64
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient
from adspygoogle.common import Utils


# Set the parameters for the In-Stream video asset.
ASSET_NAME = 'INSERT_ASSET_NAME_HERE'
PATH_TO_FILE = 'INSERT_PATH_TO_FILE_HERE'
IN_STREAM_VIDEO_CREATIVE_ID = 'INSERT_IN_STREAM_VIDEO_CREATIVE_ID_HERE'
ASSET_TO_REPLACE = 'INSERT_ASSET_TO_REPLACE_HERE'


def main(client, asset_name, path_to_file, in_stream_video_creative_id,
         asset_to_replace):
  # Initialize appropriate service.
  creative_service = client.GetCreativeService(
      'https://advertisersapitest.doubleclick.net', 'v1.19')

  # Convert file into format that can be sent in SOAP messages.
  content = Utils.ReadFile(path_to_file)
  content = base64.encodestring(content)

  # Create the In-Stream video creative asset.
  in_stream_video_asset = {
      'name': asset_name,
      'content': content,
  }

  # Create an upload request to make this asset a media file for an existing
  # In-Stream creative.
  in_stream_asset_upload_request = {
      'companion': 'true',
      'inStreamAsset': in_stream_video_asset,
      'creativeId': in_stream_video_creative_id
  }

  # Replace the existing asset with a newly uploaded asset.
  result = creative_service.ReplaceInStreamAsset(
      asset_to_replace, in_stream_asset_upload_request)[0]

  # Display a success message.
  print ('Replaced companion ad asset \'%s\' in In-Stream video creative with '
         'ID \'%s\'.' % (asset_to_replace, result['id']))


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, ASSET_NAME, PATH_TO_FILE, IN_STREAM_VIDEO_CREATIVE_ID,
       ASSET_TO_REPLACE)
