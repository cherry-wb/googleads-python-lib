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

This example is intended for users who wish to use the oauth2client library
directly. Using a workflow similar to the example here, you can take advantage
of the oauth2client in a broader range of contexts than caching your refresh
token using the config.py scripts allows.

You can avoid having to use the oauth2client library directly by using the Ads
Python Client Library's config.py script to cache a client ID, client secret,
and refresh token for reuse.

This example is intended to be run from the command line as it takes user input.
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import httplib2
import os
import sys

sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
from adspygoogle import AdWordsClient
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError


email = 'INSERT_EMAIL'
client_customer_id = 'INSERT_CLIENT_CUSTOMER_ID'
# Visit https://code.google.com/apis/console to generate your client_id,
# client_secret and to register your redirect_uri.
# See the oauth2client wiki for more information on performing the OAuth2 flow:
# http://code.google.com/p/google-api-python-client/wiki/OAuth2
oauth2_client_id = 'INSERT_OAUTH2_CLIENT_ID'
oauth2_client_secret = 'INSERT_OAUTH2_CLIENT_SECRET'


def main(email, client_customer_id, oauth2_client_id,
         oauth2_client_secret):
  # We're using the oauth2client library:
  # http://code.google.com/p/google-api-python-client/downloads/list
  flow = OAuth2WebServerFlow(
      client_id=oauth2_client_id,
      client_secret=oauth2_client_secret,
      # Scope is the server address with '/api/adwords' appended.
      scope='https://adwords.google.com/api/adwords',
      user_agent='oauth2 code example',
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  # Get the authorization URL to direct the user to.
  authorize_url = flow.step1_get_authorize_url()

  print ('Log in to your AdWords account and open the following URL: \n%s\n' %
         authorize_url)
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  credential = None
  try:
    credential = flow.step2_exchange(code)
  except FlowExchangeError, e:
    sys.exit('Authentication has failed: %s' % e)

  # Create the AdWordsUser and set the OAuth2 credentials.
  client = AdWordsClient(headers={
      'developerToken': '%s++USD' % email,
      'clientCustomerId': client_customer_id,
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

  campaign_service = client.GetCampaignService(version='v201302')

  # Get all campaigns.
  # Construct selector and get all campaigns.
  selector = {
      'fields': ['Id', 'Name', 'Status']
  }
  campaigns = campaign_service.Get(selector)[0]

  # Display results.
  if 'entries' in campaigns:
    for campaign in campaigns['entries']:
      print ('Campaign with id \'%s\', name \'%s\' and status \'%s\' was found.'
             % (campaign['id'], campaign['name'], campaign['status']))
  else:
    print 'No campaigns were found.'

  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201302')

  # Create report definition.
  report = {
      'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
      'dateRangeType': 'LAST_7_DAYS',
      'reportType': 'CRITERIA_PERFORMANCE_REPORT',
      'downloadFormat': 'CSV',
      'selector': {
          'fields': ['CampaignId', 'AdGroupId', 'Id', 'CriteriaType',
                     'Criteria', 'Impressions', 'Clicks', 'Cost']
      },
      # Enable to get rows with zero impressions.
      'includeZeroImpressions': 'false'
  }

  print report_downloader.DownloadReport(report)


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(email, client_customer_id, oauth2_client_id,
       oauth2_client_secret)
