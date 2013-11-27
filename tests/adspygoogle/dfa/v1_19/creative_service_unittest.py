#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unit tests to cover CreativeService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import base64
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa.v1_19 import client
from tests.adspygoogle.dfa.v1_19 import HTTP_PROXY
from tests.adspygoogle.dfa.v1_19 import SERVER_V1_19
from tests.adspygoogle.dfa.v1_19 import VERSION_V1_19


class CreativeServiceTestV1_19(unittest.TestCase):

  """Unittest suite for CreativeService using v1_19."""

  SERVER = SERVER_V1_19
  VERSION = VERSION_V1_19
  client.debug = False
  test_rich_media = False
  service = None
  campaign = None
  creative_id = '0'
  creative_asset = None
  placement_id = '0'
  creative_group_id = '0'
  upload_session_id = '0'
  creative_upload_session_object = None
  richmedia_asset = None
  richmedia_package = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign is None:
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.campaign = campaign_service.GetCampaignsByCriteria(
          search_criteria)[0]['records'][0]

    if self.__class__.placement_id == '0':
      placement_service = client.GetPlacementService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      placement_search_criteria = {
          'campaignIds': [self.__class__.campaign['id']]
      }
      self.__class__.placement_id = placement_service.GetPlacementsByCriteria(
          placement_search_criteria)[0]['records'][0]['id']

    if self.__class__.creative_group_id == '0':
      creative_group_service = client.GetCreativeGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      creative_group = {
          'advertiserId': self.__class__.campaign['advertiserId'],
          'groupNumber': '1',
          'name': 'Group #%s' % Utils.GetUniqueName(),
          'id': '-1'
      }
      self.__class__.creative_group_id = \
          creative_group_service.SaveCreativeGroup(creative_group)[0]['id']

      if self.__class__.campaign['creativeGroupIds'] is None:
        self.__class__.campaign['creativeGroupIds'] = \
            [self.__class__.creative_group_id]
      else:
        self.__class__.campaign['creativeGroupIds'].append(
            self.__class__.creative_group_id)
      campaign_service.SaveCampaign(self.__class__.campaign)

  def testSaveCreative(self):
    """Test whether we can save a creative."""
    pass
    if self.__class__.creative_asset is None:
      self.testSaveCreativeAsset()
    campaign_id = self.__class__.campaign['id']
    advertiser_id = self.__class__.campaign['advertiserId']
    size_id = self.__class__.creative_asset['size']['id']
    asset_filename = self.__class__.creative_asset['savedFilename']
    creative = {
        'xsi_type': 'ImageCreative',
        'name': 'Creative #%s' % Utils.GetUniqueName(),
        'typeId': '1', #image
        'sizeId': size_id,
        'assetFilename': asset_filename,
        'alternateText': 'Created by the python client library unit test.',
        'advertiserId' : advertiser_id
    }
    creative = self.__class__.service.SaveCreative(creative, campaign_id)
    self.__class__.creative_id = creative[0]['id']
    self.assert_(isinstance(creative, tuple))

  def testDeleteCreative(self):
    """Test whether we can delete a creative."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    self.assertEqual(self.__class__.service.DeleteCreative(
        self.__class__.creative_id), None)
    self.__class__.creative_id = '0'

  def testGetCreative(self):
    """Test whether we can fetch a creative by id."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    creative_id = self.__class__.creative_id
    self.assert_(isinstance(self.__class__.service.GetCreative(
        creative_id), tuple))

  def testGetCreatives(self):
    """Test whether we can fetch creatives by criteria."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    search_criteria = {
        'ids': [self.__class__.creative_id],
        'campaignId': self.__class__.campaign['id']
    }
    self.assert_(isinstance(self.__class__.service.GetCreatives(
        search_criteria), tuple))

  def testGetCreativeTypes(self):
    """Test whether we can fetch creative types."""
    self.assert_(isinstance(
        self.__class__.service.GetCreativeTypes(), tuple))

  def testSaveCreativeAsset(self):
    """Test whether we can save a creative asset."""
    advertiser_id = self.__class__.campaign['advertiserId']
    content = Utils.ReadFile(os.path.join('..', 'data', 'code_logo.gif'))
    content = base64.encodestring(content)
    creative_asset = {
        'name': 'CreativeAsset%s.gif' % Utils.GetUniqueName(),
        'advertiserId': advertiser_id,
        'forHTMLCreatives': 'false',
        'content': content,
    }
    creative_asset = self.__class__.service.SaveCreativeAsset(creative_asset)
    self.__class__.creative_asset = creative_asset[0]
    self.assert_(isinstance(creative_asset, tuple))

  def testGetCreativeAssets(self):
    """Test whether we can fetch creative assets by criteria."""
    if self.__class__.creative_asset is None:
      self.testSaveCreativeAsset()
    search_criteria = {
        'advertiserId': self.__class__.campaign['advertiserId'],
        'assetFilename': self.__class__.creative_asset['savedFilename']
    }
    self.assert_(isinstance(self.__class__.service.GetCreativeAssets(
        search_criteria), tuple))

  def testAssignCreativesToPlacements(self):
    """Test whether we can assign creatives to placements."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    creative_id = self.__class__.creative_id
    placement_id = self.__class__.placement_id
    creative_placement_assignments = [{
        'adName': 'Ad #%s' % Utils.GetUniqueName(),
        'creativeId': creative_id,
        'placementId': placement_id,
        'placementIds': [placement_id, placement_id]
    }]
    creative_placement_assignments = \
        self.__class__.service.AssignCreativesToPlacements(
            creative_placement_assignments)
    self.assert_(isinstance(creative_placement_assignments, tuple))

  def testAssociateCreativesToCampaign(self):
    """Test whether we can associate creatives to a campaign."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    campaign_id = self.__class__.campaign['id']
    creative_id = self.__class__.creative_id
    self.assert_(isinstance(self.__class__.service.AssociateCreativesToCampaign(
        campaign_id, [creative_id]), tuple))

  def testCopyCreative(self):
    """Test whether we can copy a creative."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    advertiser_id = self.__class__.campaign['advertiserId']
    campaign_id = self.__class__.campaign['id']
    creative_id = self.__class__.creative_id
    creative_copy_request = {
        'advertiserId': advertiser_id,
        'campaignId': campaign_id,
        'creativeId': creative_id,
        'copyMode': '0'
    }
    self.assert_(isinstance(self.__class__.service.CopyCreative(
        [creative_copy_request, creative_copy_request]), tuple))

  def testGenerateCreativeUploadSession(self):
    """Test whether we can generate a creative upload session."""
    campaign_id = self.__class__.campaign['id']
    advertiser_id = self.__class__.campaign['advertiserId']
    creative_upload_session_request = {
        'campaignId': campaign_id,
        'advertiserId': advertiser_id
    }
    creative_upload_session_request = \
        self.__class__.service.GenerateCreativeUploadSession(
            creative_upload_session_request)
    self.__class__.upload_session_id = \
        creative_upload_session_request[0]['creativeUploadId']
    self.assert_(isinstance(creative_upload_session_request, tuple))

  def testCreateCreativesFromCreativeUploadSession(self):
    """Test whether we can create creatives from a creative upload session."""
    if self.__class__.creative_upload_session_object is None:
      self.testUploadCreativeFiles()
    campaign_id = self.__class__.campaign['id']
    advertiser_id = self.__class__.campaign['advertiserId']
    upload_session_id = self.__class__.upload_session_id
    image_file_id = self.__class__.creative_upload_session_object[
        'uploadedFiles'][0]['id']
    image_file_name = self.__class__.creative_upload_session_object[
        'uploadedFiles'][0]['name']
    creative_upload_session = {
        'campaignId': campaign_id,
        'creativeUploadId': upload_session_id,
        'advertiserId': advertiser_id,
        'creativeSaveRequests': [{
            'imageFile': {
                'id': image_file_id,
                'name': image_file_name
            }
        }]
    }
    self.assert_(isinstance(
        self.__class__.service.CreateCreativesFromCreativeUploadSession(
            creative_upload_session), tuple))

  def testGetCompleteCreativeUploadSession(self):
    """Test whether we can fetch a complete creative upload session."""
    if self.__class__.upload_session_id == '0':
      self.testGenerateCreativeUploadSession()
    campaign_id = self.__class__.campaign['id']
    advertiser_id = self.__class__.campaign['advertiserId']
    upload_session_id = self.__class__.upload_session_id
    creative_upload_session_summary = {
        'campaignId': campaign_id,
        'advertiserId': advertiser_id,
        'creativeUploadId': upload_session_id
    }
    creative_upload_session_summary = \
        self.__class__.service.GetCompleteCreativeUploadSession(
            creative_upload_session_summary)
    self.assert_(isinstance(creative_upload_session_summary, tuple))

  def testUploadCreativeFiles(self):
    """Test whether we can upload creative files in a creative upload
    session."""
    if self.__class__.upload_session_id == '0':
      self.testGenerateCreativeUploadSession()
    campaign_id = self.__class__.campaign['id']
    advertiser_id = self.__class__.campaign['advertiserId']
    upload_session_id = self.__class__.upload_session_id
    content = Utils.ReadFile(os.path.join('..', 'data', 'code_logo.gif'))
    content = base64.encodestring(content)
    creative_upload_request = {
        'creativeUploadSessionSummary': {
            'campaignId': campaign_id,
            'advertiserId': advertiser_id,
            'creativeUploadId': upload_session_id
        },
        'rawFiles': [{
            'filename': 'UploadedFile%s.gif' % Utils.GetUniqueName(),
            'mimeType': 'image/gif',
            'fileData': content
        }]
    }
    creative_upload_request = self.__class__.service.UploadCreativeFiles(
            creative_upload_request)
    self.__class__.creative_upload_session_object = creative_upload_request[0]
    self.assert_(isinstance(creative_upload_request, tuple))

  def testGetCreativeRenderings(self):
    """Test whether we can fetch creative renderings."""
    if self.__class__.creative_id == '0':
      self.testSaveCreative()
    creative_id = self.__class__.creative_id
    creative_rendering_request = {
        'creativeIds': [creative_id]
    }
    self.assert_(isinstance(self.__class__.service.GetCreativeRenderings(
        creative_rendering_request), tuple))

  # The following tests are only for networks which support Rich Media
  def testUploadRichMediaAsset(self):
    """Test whether we can upload a RichMedia asset."""
    if self.__class__.test_rich_media:
      content = Utils.ReadFile(os.path.join('..', 'data', 'Inpage.mtf'))
      content = base64.encodestring(content)
      upload_request = {
          'assetFileName': 'RichmediaAsset%s.mtf' % Utils.GetUniqueName(),
          'fileData': content
      }
      upload_request = self.__class__.service.UploadRichMediaAsset(
              upload_request)
      self.__class__.richmedia_asset = upload_request[0]
      self.assert_(isinstance(upload_request, tuple))

  def testUploadRichMediaCreativePackage(self):
    """Test whether we can upload the mtf file creative the RichMedia
    creative."""
    if self.__class__.test_rich_media:
      advertiser_id = self.__class__.campaign['advertiserId']
      content = Utils.ReadFile(os.path.join('..', 'data', 'Inpage.mtf'))
      content = base64.encodestring(content)
      rich_media = self.__class__.service.UploadRichMediaCreativePackage(
              advertiser_id, content, 'False')
      self.__class__.richmedia_package = upload_request[0]
      self.assert_(isinstance(rich_media, tuple))

  def testDeleteRichMediaAsset(self):
    """Test whether we can delete a rich media asset."""
    if self.__class__.test_rich_media:
      if self.__class__.richmedia_asset is None:
        self.testUploadRichMediaAsset()
      self.assert_(isinstance(
          self.__class__.service.DeleteRichMediaAsset(
          self.__class__.richmedia_asset['id'],
          self.__class__.richmedia_asset['childAssets'][0]['fileName']), tuple))
      self.__class__.richmedia_asset = None

  def testGetRichMediaPreviewUrl(self):
    """Test whether we can fetch the default external preview URL for a
    RichMedia Creative."""
    if self.__class__.test_rich_media:
      if self.__class__.richmedia_asset is None:
        self.testUploadRichMediaAsset()
      self.assert_(isinstance(
          self.__class__.service.DeleteRichMediaAsset(
          self.__class__.richmedia_asset['id'],
          self.__class__.richmedia_asset['childAssets'][0]['fileName']), tuple))

  def testReplaceRichMediaAsset(self):
    """Test whether we can replace a RichMedia asset with the object passed."""
    if self.__class__.test_rich_media:
      if self.__class__.richmedia_asset is None:
        self.testUploadRichMediaAsset()
      content = Utils.ReadFile(os.path.join('..', 'data', 'Inpage.mtf'))
      content = base64.encodestring(content)
      replace_request = {
          'assetFileName': 'RichmediaAsset%s.mtf' % Utils.GetUniqueName(),
          'creativeId': self.__class__.richmedia_asset['id'],
          'fileData': content
      }
      self.assert_(isinstance(
          self.__class__.service.ReplaceRichMediaAsset(
          self.__class__.richmedia_asset['childAssets'][0]['fileName'],
          replace_request), tuple))

  def testReplaceRichMediaCreativePackage(self):
    """Test whether we can replace the mtf for the creative."""
    if self.__class__.test_rich_media:
      if self.__class__.richmedia_package is None:
        self.testUploadRichMediaCreativePackage()
      content = Utils.ReadFile(os.path.join('..', 'data', 'Inpage.mtf'))
      content = base64.encodestring(content)
      self.assert_(isinstance(
          self.__class__.service.ReplaceRichMediaCreativePackage(
          self.__class__.richmedia_package['id'], content), tuple))


if __name__ == '__main__':
  unittest.main()
