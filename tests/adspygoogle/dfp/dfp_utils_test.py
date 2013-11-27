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

"""Unit tests to cover DfpUtils."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock
from adspygoogle import DfpClient
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import DfpUtils


class DfpUtilsTest(unittest.TestCase):

  """Unittest suite for DfpUtils."""

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in DfpUtils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in DfpUtils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    client = mock.Mock()
    line_item_service = mock.Mock()
    rval = 'Line items for everyone!'

    def VerifyExpectedCall(arg):
      self.assertEqual({'values': None,
                        'query': 'ORDER BY name LIMIT 500 OFFSET 0'}, arg)
      return [{'results': [rval]}]

    client.GetLineItemService.return_value = line_item_service
    line_item_service._service_name = 'LineItemService'
    line_item_service.GetLineItemsByStatement.side_effect = VerifyExpectedCall

    line_items = DfpUtils.GetAllEntitiesByStatement(
        client, 'LineItem', 'ORDER BY name')
    self.assertEqual([rval], line_items)

  def testGetAllEntitiesByStatementWithLimit(self):
    """Test whether GetAllEntitiesByStatement() fails when LIMIT is provided."""
    headers = {
        'email': 'fake_email',
        'password': 'fake_password',
        'applicationName': 'fake_application_name',
        'authToken': ' '
    }
    client = DfpClient(headers=headers)
    self.failUnlessRaises(
        ValidationError, DfpUtils.GetAllEntitiesByStatement,
        client, 'User', 'ORDER BY name LIMIT 1')

  def testGetAllEntitiesByStatementWithService(self):
    line_item_service = mock.Mock()
    rval = 'Line items for everyone!'

    def VerifyExpectedCall(arg):
      self.assertEqual({'values': None,
                        'query': 'ORDER BY name LIMIT 500 OFFSET 0'}, arg)
      return [{'results': [rval]}]

    line_item_service._service_name = 'LineItemService'
    line_item_service.GetLineItemsByStatement.side_effect = VerifyExpectedCall

    line_items = DfpUtils.GetAllEntitiesByStatementWithService(
        line_item_service, 'ORDER BY name')
    self.assertEqual([rval], line_items)

  def testDownloadPqlResultSetToCsv(self):
    pql_service = mock.Mock()
    csv_file = tempfile.NamedTemporaryFile()
    csv_file_name = csv_file.name

    header = [{'labelName': 'Some random header...'},
              {'labelName': 'Another header...'}]
    rval = [{'values': [{'value': 'Some random PQL response...',
                         'Value_Type': 'TextValue'},
                        {'value': {'date': {
                            'year': '1999', 'month': '04', 'day': '03'}},
                         'Value_Type': 'DateValue'},
                        {'value': '123',
                         'Value_Type': 'NumberValue'},
                        {'value': {'date': {'year': '2012',
                                            'month': '11',
                                            'day': '05'},
                                   'hour': '12',
                                   'minute': '12',
                                   'second': '12',
                                   'timeZoneID': 'PST8PDT'},
                         'Value_Type': 'DateTimeValue'}]},
            {'values': [{'value': 'A second row of PQL response!',
                         'Value_Type': 'TextValue'},
                        {'value': {'date': {
                            'year': '2009', 'month': '02', 'day': '05'}},
                         'Value_Type': 'DateValue'},
                        {'value': '345',
                         'Value_Type': 'NumberValue'},
                        {'value': {'date': {'year': '2013',
                                            'month': '01',
                                            'day': '03'},
                                   'hour': '02',
                                   'minute': '02',
                                   'second': '02',
                                   'timeZoneID': 'GMT'},
                         'Value_Type': 'DateTimeValue'}]}]

    def VerifyExpectedCall(arg):
      self.assertEqual({'values': None,
                        'query': ('SELECT Id, Name FROM Line_Item '
                                  'LIMIT 500 OFFSET 0')}, arg)
      return [{'rows': rval, 'columnTypes': header}]

    pql_service._service_name = 'PublisherQueryLanguageService'
    pql_service.select.side_effect = VerifyExpectedCall

    file_returned = DfpUtils.DownloadPqlResultSetToCsv(
        pql_service, 'SELECT Id, Name FROM Line_Item', csv_file)

    self.assertEqual(file_returned.name, csv_file_name)
    self.assertEqual(file_returned.readline(),
                     ('"Some random header...",'
                      '"Another header..."\r\n'))
    self.assertEqual(file_returned.readline(),
                     ('"Some random PQL response...",'
                      '"1999-04-03",'
                      '123,'
                      '"2012-11-05T12:12:12-08:00"\r\n'))
    self.assertEqual(file_returned.readline(),
                     ('"A second row of PQL response!",'
                      '"2009-02-05",'
                      '345,'
                      '"2013-01-03T02:02:02Z"\r\n'))
    csv_file.close()

  def testDownloadPqlResultToList(self):
    pql_service = mock.Mock()
    header = [{'labelName': 'Some random header...'},
              {'labelName': 'Another header...'}]
    rval = [{'values': [{'value': 'Some random PQL response...',
                         'Value_Type': 'TextValue'},
                        {'value': {'date': {
                            'year': '1999', 'month': '04', 'day': '03'}},
                         'Value_Type': 'DateValue'},
                        {'value': '123',
                         'Value_Type': 'NumberValue'},
                        {'value': {'date': {'year': '2012',
                                            'month': '11',
                                            'day': '05'},
                                   'hour': '12',
                                   'minute': '12',
                                   'second': '12',
                                   'timeZoneID': 'PST8PDT'},
                         'Value_Type': 'DateTimeValue'}]},
            {'values': [{'value': 'A second row of PQL response!',
                         'Value_Type': 'TextValue'},
                        {'value': {'date': {
                            'year': '2009', 'month': '02', 'day': '05'}},
                         'Value_Type': 'DateValue'},
                        {'value': '345',
                         'Value_Type': 'NumberValue'},
                        {'value': {'date': {'year': '2013',
                                            'month': '01',
                                            'day': '03'},
                                   'hour': '02',
                                   'minute': '02',
                                   'second': '02',
                                   'timeZoneID': 'GMT'},
                         'Value_Type': 'DateTimeValue'}]}]

    def VerifyExpectedCall(arg):
      self.assertEqual({'values': None,
                        'query': ('SELECT Id, Name FROM Line_Item '
                                  'LIMIT 500 OFFSET 0')}, arg)
      return [{'rows': rval, 'columnTypes': header}]

    pql_service._service_name = 'PublisherQueryLanguageService'
    pql_service.select.side_effect = VerifyExpectedCall

    result_set = DfpUtils.DownloadPqlResultToList(
        pql_service, 'SELECT Id, Name FROM Line_Item')

    row1 = [DfpUtils._ConvertValueForCsv(field) for field in rval[0]['values']]
    row2 = [DfpUtils._ConvertValueForCsv(field) for field in rval[1]['values']]

    self.assertEqual([[header[0]['labelName'], header[1]['labelName']],
                      row1, row2], result_set)

  def testFilterStatement(self):
    values = [{
        'key': 'test_key',
        'value': {
            'xsi_type': 'TextValue',
            'value': 'test_value'
        }
    }]
    test_statement = DfpUtils.FilterStatement()
    self.assertEqual(test_statement.ToStatement(),
                     {'query': ' LIMIT 500 OFFSET 0',
                      'values': None})
    test_statement.IncreaseOffsetBy(30)
    self.assertEqual(test_statement.ToStatement(),
                     {'query': ' LIMIT 500 OFFSET 30',
                      'values': None})
    test_statement.offset = 123
    test_statement.limit = 5
    self.assertEqual(test_statement.ToStatement(),
                     {'query': ' LIMIT 5 OFFSET 123',
                      'values': None})
    test_statement = DfpUtils.FilterStatement(
        'SELECT Id FROM Line_Item WHERE key = :test_key', limit=300, offset=20,
        values=values)
    self.assertEqual(test_statement.ToStatement(),
                     {'query': 'SELECT Id FROM Line_Item WHERE key = '
                               ':test_key LIMIT 300 OFFSET 20',
                      'values': values})


if __name__ == '__main__':
  unittest.main()
