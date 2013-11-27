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

"""This example creates an In-Stream video creative associated with a given
advertiser. If a campaign is specified, the creative is also associated with
that campaign.

To associate In-Stream assets with an In-Stream video creative, first create
the creative and then run upload_in_stream_asset.py.

Tags: creative.saveCreative
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient
from adspygoogle.common import Utils


# Set the parameters for the new In-Stream video creative.
ADVERTISER_ID = 'INSERT_ADVERTISER_ID_HERE'
VIDEO_DURATION = 'INSERT_VIDEO_DURATION_HERE'
AD_ID = 'INSERT_VAST_AD_ID_HERE'
SURVEY_URL = 'INSERT_VAST_SURVEY_URL_HERE'
CLICK_THROUGH_URL = 'INSERT_VAST_CLICK_THROUGH_URL_HERE'
# You may optionally set a campaign ID. If the campaign ID is set to 0, then the
# creative will be associated only with the advertiser.
CAMPAIGN_ID = '0'


def main(client, advertiser_id, video_duration, ad_id, survey_url,
         click_through_url, campaign_id):
  # Initialize appropriate service.
  creative_service = client.GetCreativeService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Create the In-Stream video creative.
  in_stream_video_creative = {
      'advertiserId': advertiser_id,
      'name': 'In-Stream Video Creative #%s' % Utils.GetUniqueName(),
      'videoDuration': video_duration,
      # In-Stream video creatives have to be created inactive. One can only be
      # set active after at least one media file has been added to it or the API
      # will return an error message.
      'active': 'false',

      # Set the video details based on the Video Ad Serving Template (VAST)
      # specification.
      'adId': ad_id,
      'description': 'You are viewing an In-Stream Video Creative',
      'surveyUrl': survey_url,
      'clickThroughUrl': click_through_url
  }

  # Save the In-Stream video creative.
  result = creative_service.SaveCreative(
      in_stream_video_creative, campaign_id)[0]

  # Display the new creative ID.
  print 'In-Stream video creative with ID \'%s\' was created.' % result['Id']


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, ADVERTISER_ID, VIDEO_DURATION, AD_ID, SURVEY_URL,
       CLICK_THROUGH_URL, CAMPAIGN_ID)
