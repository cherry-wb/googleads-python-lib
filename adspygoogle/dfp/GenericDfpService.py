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

"""Generic proxy to access any DFP web service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import time

from adspygoogle import SOAPpy
from adspygoogle.common import Utils
from adspygoogle.common.Errors import Error
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.GenericApiService import GenericApiService
from adspygoogle.common.GenericApiService import MethodInfoKeys
from adspygoogle.dfp import AUTH_TOKEN_EXPIRE
from adspygoogle.dfp import AUTH_TOKEN_SERVICE
from adspygoogle.dfp import LIB_SIG
from adspygoogle.dfp import LIB_URL
from adspygoogle.dfp.DfpErrors import DfpApiError
from adspygoogle.dfp.DfpErrors import DfpError
from adspygoogle.dfp.DfpErrors import ERRORS
from adspygoogle.dfp.DfpSoapBuffer import DfpSoapBuffer


class GenericDfpService(GenericApiService):

  """Wrapper for any DFP web service."""

  # The _IGNORED_HEADER_VALUES are keys in the headers dictionary passed into
  # this class' constuctor which should NOT be packed into the SOAP header.
  _IGNORED_HEADER_VALUES = ('authToken', 'email', 'password',
                            'oauth2credentials')
  # The _WRAP_LISTS constant indicates that DFP services do not need to wrap
  # lists in an extra layer of XML element tags.
  _WRAP_LISTS = False
  # The _BUFFER_CLASS is the subclass of SoapBuffer that should be used to track
  # all SOAP interactions
  _BUFFER_CLASS = DfpSoapBuffer

  def __init__(self, headers, config, op_config, lock, logger, service_name):
    """Inits GenericDfpService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock to use to synchronize requests.
      logger: Logger Instance of Logger to use for logging.
      service_name: string The name of this service.
    """
    service_url = '/'.join([op_config['server'], 'apis/ads/publisher',
                            op_config['version'], service_name])
    namespace = '/'.join(['https://www.google.com/apis/ads/publisher',
                          op_config['version']])
    namespace_extractor = _DetermineNamespacePrefix

    super(GenericDfpService, self).__init__(
        headers, config, op_config, lock, logger, service_name, service_url,
        GenericDfpService._WRAP_LISTS, GenericDfpService._BUFFER_CLASS,
        namespace, namespace_extractor)

    # DFP-specific changes to the SOAPpy.WSDL.Proxy
    methodattrs = {
        'xmlns:dfp': self._namespace,
        'xmlns': self._namespace
    }
    self._soappyservice.soapproxy.methodattrs = methodattrs

  def _SetHeaders(self):
    """Sets the SOAP headers for this service's requests."""
    now = time.time()
    if ((('authToken' not in self._headers and
          'auth_token_epoch' not in self._config) or
         int(now - self._config['auth_token_epoch']) >= AUTH_TOKEN_EXPIRE) and
        not self._headers.get('oauth2credentials')):
      if ('email' not in self._headers or not self._headers['email'] or
          'password' not in self._headers or not self._headers['password']):
        raise ValidationError('Required authentication headers, \'email\' and '
                              '\'password\', are missing. Unable to regenerate '
                              'authentication token.')
      self._headers['authToken'] = Utils.GetAuthToken(
          self._headers['email'], self._headers['password'], AUTH_TOKEN_SERVICE,
          LIB_SIG, self._config['proxy'])
      self._config['auth_token_epoch'] = time.time()

    # Apply headers to the SOAPpy service.
    soap_headers = SOAPpy.Types.headerType(attrs={'xmlns': self._namespace})
    request_header_data = {}
    if 'authToken' in self._headers:
      authentication_block = SOAPpy.Types.structType(
          data={'token': self._headers['authToken']},
          name='authentication', typed=0,
          attrs={(SOAPpy.NS.XSI3, 'type'): 'ClientLogin'})
      request_header_data['authentication'] = authentication_block
    for key in self._headers:
      if (key in GenericDfpService._IGNORED_HEADER_VALUES or
          not self._headers[key]):
        continue
      request_header_data[key] = SOAPpy.Types.stringType(self._headers[key])
    request_header = SOAPpy.Types.structType(
        data=request_header_data, name='RequestHeader', typed=0)
    soap_headers.RequestHeader = request_header
    if 'authToken' in self._headers:
      soap_headers.RequestHeader._keyord = ['applicationName', 'authentication']
    self._soappyservice.soapproxy.header = soap_headers

  def _GetMethodInfo(self, method_name):
    """Pulls all of the relevant data about a method from a SOAPpy service.

    The return dictionary has two keys, MethodInfoKeys.INPUTS and
    MethodInfoKeys.OUTPUTS. Each of these keys has a list value. These lists
    contain a dictionary of information on the input/output parameter list, in
    order.

    Args:
      method_name: string The name of the method to pull information for.
    Returns:
      dict A dictionary containing information about a SOAP method.
    """
    rval = {}
    rval[MethodInfoKeys.INPUTS] = []
    for i in range(len(self._soappyservice.wsdl.types[
        self._namespace].elements[method_name].content.content.content)):
      param_attributes = self._soappyservice.wsdl.types[
          self._namespace].elements[method_name].content.content.content[
              i].attributes
      inparam = {
          MethodInfoKeys.ELEMENT_NAME: param_attributes['name'],
          MethodInfoKeys.NS: param_attributes['type'].getTargetNamespace(),
          MethodInfoKeys.TYPE: param_attributes['type'].getName(),
          MethodInfoKeys.MAX_OCCURS: param_attributes['maxOccurs']
      }
      rval[MethodInfoKeys.INPUTS].append(inparam)

    rval[MethodInfoKeys.OUTPUTS] = []
    for i in range(len(self._soappyservice.wsdl.types[
        self._namespace].elements[
            method_name + 'Response'].content.content.content)):
      param_attributes = self._soappyservice.wsdl.types[
          self._namespace].elements[
              method_name + 'Response'].content.content.content[i].attributes
      outparam = {
          MethodInfoKeys.ELEMENT_NAME: param_attributes['name'],
          MethodInfoKeys.NS: param_attributes['type'].getTargetNamespace(),
          MethodInfoKeys.TYPE: param_attributes['type'].getName(),
          MethodInfoKeys.MAX_OCCURS: param_attributes['maxOccurs']
      }
      rval[MethodInfoKeys.OUTPUTS].append(outparam)
    return rval

  def _HandleLogsAndErrors(self, buf, start_time, stop_time, error=None):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      start_time: str Time before service call was invoked.
      stop_time: str Time after service call was invoked.
      [optional]
      error: dict Error, if any.
    """
    if error is None:
      error = {}
    try:
      handlers = self.__GetLogHandlers(buf)

      fault = super(GenericDfpService, self)._ManageSoap(
          buf, handlers, LIB_URL, start_time, stop_time, error)
      if fault:
        # Raise a specific error, subclass of DfpApiError.
        if 'detail' in fault:
          if 'code' in fault['detail']:
            code = int(fault['detail']['code'])
            if code in ERRORS: raise ERRORS[code](fault)
          elif 'errors' in fault['detail']:
            error_type = fault['detail']['errors'][0]['type']
            if error_type in ERRORS: raise ERRORS[str(error_type)](fault)

        if isinstance(fault, basestring):
          raise DfpError(fault)
        elif isinstance(fault, dict):
          raise DfpApiError(fault)
    except DfpApiError, e:
      raise e
    except DfpError, e:
      raise e
    except Error, e:
      if error: e = error
      raise Error(e)

  def __GetLogHandlers(self, buf):
    """Gets a list of log handlers for the DFP library.

    Args:
      buf: SoapBuffer SOAP buffer from which calls are retrieved for logging.

    Returns:
      list Log handlers for the DFP library.
    """
    return [
        {
            'tag': 'xml_log',
            'name': 'soap_xml',
            'data': ''
        },
        {
            'tag': 'request_log',
            'name': 'request_info',
            'data': str('host=%s service=%s method=%s responseTime=%s '
                        'requestId=%s'
                        % (Utils.GetNetLocFromUrl(self._service_url),
                           self._service_name, buf.GetCallName(),
                           buf.GetCallResponseTime(), buf.GetCallRequestId()))
        },
        {
            'tag': '',
            'name': 'dfp_api_lib',
            'data': ''
        }
    ]


def _DetermineNamespacePrefix(url):
  """Returns the SOAP prefix to use for definitions within the given namespace.

  Args:
    url: string The URL of the namespace.

  Returns:
    string The SOAP namespace prefix to use for the given namespace.
  """
  return 'dfp:'
