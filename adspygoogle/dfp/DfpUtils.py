#!/usr/bin/python
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

"""Handy utility functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import csv
import datetime
import gzip
import os
import StringIO
import time
import urllib

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import DEFAULT_API_VERSION
from adspygoogle.dfp import LIB_HOME
import pytz

PAGE_LIMIT = 500


def GetCurrencies():
  """Get a list of available currencies.

  Returns:
    list available currencies.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'currencies.csv'))


def GetTimezones():
  """Get a list of available timezones.

  Returns:
    list Available timezones.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'timezones.csv'))


def GetAllEntitiesByStatement(client, service_name, query='', page_size=500,
                              server='https://www.google.com',
                              version=DEFAULT_API_VERSION, http_proxy=None):
  """Get all existing entities by statement.

  All existing entities are retrieved for a given statement and page size. The
  retrieval of entities works across all services. Thus, the same method can
  be used to fetch companies, creatives, ad units, line items, etc. The results,
  even if they span multiple pages, are grouped into a single list of entities.

  Args:
    client: Client an instance of Client.
    service_name: str name of the service to use.
    [optional]
    query: str a statement filter to apply, if any. The default is empty string.
    page_size: int size of the page to use. If page size is less than 0 or
               greater than 500, defaults to 500.
    server: str API server to access for this API call. The default value is
            'https://www.google.com'.
    version: str API version to use.
    http_proxy: str HTTP proxy to use.

  Returns:
    list a list of existing entities.
  """
  service = eval('client.Get%sService(server, version, http_proxy)'
                 % service_name)
  return GetAllEntitiesByStatementWithService(service, query, page_size)


def GetAllEntitiesByStatementWithService(service, query='', page_size=500,
                                         bind_vars=None):
  """Get all existing entities by statement.

  All existing entities are retrieved for a given statement and page size. The
  retrieval of entities works across all services. Thus, the same method can
  be used to fetch companies, creatives, ad units, line items, etc. The results,
  even if they span multiple pages, are grouped into a single list of entities.

  Args:
    service: ApiService an instance of the service to use.
    [optional]
    query: str a statement filter to apply, if any. The default is empty string.
    page_size: int size of the page to use. If page size is less than 0 or
               greater than 500, defaults to 500.
    bind_vars: list Key value pairs of bind variables to use with query.

  Returns:
    list a list of existing entities.
  """

  service_name = service._service_name[0:service._service_name.rfind('Service')]

  if service_name == 'Inventory':
    service_name = 'AdUnit'
  if service_name[-1] == 'y':
    method_name = service_name[:-1] + 'ies'
  else:
    method_name = service_name + 's'
  if service_name == 'Content':
    method_name = service_name
  method_name = 'Get%sByStatement' % method_name

  if page_size <= 0 or page_size > 500:
    page_size = 500

  if (query and
      (query.upper().find('LIMIT') > -1 or query.upper().find('OFFSET') > -1)):
    raise ValidationError('The filter query contains an option that is '
                          'incompatible with this method.')

  offset = 0
  all_entities = []
  while True:
    filter_statement = {
        'query': '%s LIMIT %s OFFSET %s' % (query, page_size, offset),
        'values': bind_vars
    }
    entities = eval('service.%s(filter_statement)[0].get(\'results\')'
                    % method_name)

    if not entities: break
    all_entities.extend(entities)
    if len(entities) < page_size: break
    offset += page_size
  return all_entities


def _PageThroughPqlSet(pql_service, pql_query, output_function, values):
  """Pages through a pql_query and performs an action (output_function).

  Args:
    pql_service: ApiService an instance of pqlService.
    pql_query: str a statement filter to apply (the query should not include
               the limit or the offset)
    output_function: the function to call to output the results (csv or in
                     memory)
    values: list dict of bind values to use with the pql_query.
  """
  offset, result_set_size = 0, 0

  while True:
    filter_statement = {
        'query': '%s LIMIT %s OFFSET %s' % (
            pql_query, PAGE_LIMIT, offset),
        'values': values
    }
    response = pql_service.select(filter_statement)[0]

    if 'rows' in response:
      # Write the header row only on first pull
      if offset == 0:
        header = response['columnTypes']
        output_function([label['labelName'].encode('utf-8')
                         for label in header])

      entities = response['rows']
      result_set_size = len(entities)

      for entity in entities:
        output_function([_ConvertValueForCsv(value) for value
                         in entity['values']])

      offset += result_set_size
      if result_set_size != PAGE_LIMIT:
        break
    elif offset == 0:
      break


def DownloadPqlResultToList(pql_service, pql_query, values=None):
  """Downloads the results of a PQL query to a list.

  Args:
    pql_service: ApiService an instance of pqlService.
    pql_query: str a statement filter to apply (the query should not include
               the limit or the offset)
    [optional]
    values: list dict of bind values to use with the pql_query.

  Returns:
    a list of lists with the first being the header row and each subsequent
    list being a row of results.
  """
  results = []
  _PageThroughPqlSet(pql_service, pql_query, results.append, values)

  return results


def DownloadPqlResultSetToCsv(
    pql_service, pql_query, file_handle, values=None):
  """Downloads the results of a PQL query to CSV.

  Args:
    pql_service: ApiService an instance of pqlService.
    pql_query: str a statement filter to apply (the query should not include
               the limit or the offset)
    file_handle: file the file object to write to.
    [optional]
    values: list dict of bind values to use with the pql_query.

  Returns:
    the file that the data was written to.
  """
  pql_writer = csv.writer(open(file_handle.name, 'wb'), delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
  _PageThroughPqlSet(pql_service, pql_query, pql_writer.writerow, values)

  return file_handle


def _ConvertValueForCsv(pql_value):
  """Sanitizes a field value from a Value object to a CSV suitable format.

  Args:
    pql_value: dict a dictionary containing the data for a single field of an
               entity.

  Returns:
    str a CSV writer friendly value formatted by Value_Type.
  """
  field = pql_value['value']

  if pql_value['Value_Type'] == 'TextValue':
    return field.encode('utf-8')
  elif pql_value['Value_Type'] == 'NumberValue':
    return float(field) if '.' in field else int(field)
  elif pql_value['Value_Type'] == 'DateTimeValue':
    return _ConvertDateTimeToOffset(field)
  elif pql_value['Value_Type'] == 'DateValue':
    return datetime.date(int(field['date']['year']),
                         int(field['date']['month']),
                         int(field['date']['day'])).isoformat()
  else:
    return field


def _ConvertDateTimeToOffset(date_time_value):
  """Converts the PQL formatted response for a dateTime object.

  Output conforms to ISO 8061 format, e.g. 'YYYY-MM-DDTHH:MM:SSz.'

  Args:
    date_time_value: dict The date time value from the PQL response.

  Returns:
    str A string representation of the date time value uniform to ReportService.
  """
  date_time_obj = datetime.datetime(int(date_time_value['date']['year']),
                                    int(date_time_value['date']['month']),
                                    int(date_time_value['date']['day']),
                                    int(date_time_value['hour']),
                                    int(date_time_value['minute']),
                                    int(date_time_value['second']))
  date_time_str = pytz.timezone(
      date_time_value['timeZoneID']).localize(date_time_obj).isoformat()

  if date_time_str[-5:] == '00:00':
    return date_time_str[:-6] + 'Z'
  else:
    return date_time_str


def DownloadReport(report_job_id, export_format, service):
  """Download and return report data.

  Args:
    report_job_id: str ID of the report job.
    export_format: str Export format for the report file.
    service: GenericDfpService A service pointing to the ReportService.

  Returns:
    str Report data or empty string if report failed.
  """
  SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

  # Wait for report to complete.
  status = service.GetReportJob(report_job_id)[0]['reportJobStatus']
  while status != 'COMPLETED' and status != 'FAILED':
    if Utils.BoolTypeConvert(service._config['debug']):
      print 'Report job status: %s' % status
    time.sleep(30)
    status = service.GetReportJob(report_job_id)[0]['reportJobStatus']

  if status == 'FAILED':
    if Utils.BoolTypeConvert(service._config['debug']):
      print 'Report process failed'
    return ''
  else:
    if Utils.BoolTypeConvert(service._config['debug']):
      print 'Report has completed successfully'

  # Get report download URL.
  report_url = service.GetReportDownloadURL(report_job_id, export_format)[0]

  # Download report.
  data = urllib.urlopen(report_url).read()
  data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
  return data
