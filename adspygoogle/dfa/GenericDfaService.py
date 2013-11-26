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

"""Generic proxy to access any DFA web service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import warnings

from adspygoogle import SOAPpy
from adspygoogle.common import Utils
from adspygoogle.common.Errors import Error
from adspygoogle.common.GenericApiService import GenericApiService
from adspygoogle.common.GenericApiService import MethodInfoKeys
from adspygoogle.dfa import DfaUtils
from adspygoogle.dfa import LIB_SIG
from adspygoogle.dfa import LIB_URL
from adspygoogle.dfa import WSSE_NS
from adspygoogle.dfa.DfaErrors import DfaApiError
from adspygoogle.dfa.DfaErrors import DfaAuthenticationError
from adspygoogle.dfa.DfaSoapBuffer import DfaSoapBuffer


_DEPRECATION_WARNING = ('Legacy DFA passwords are deprecated. Please use '
                        'OAuth 2.0')
warnings.filterwarnings('always', _DEPRECATION_WARNING, DeprecationWarning)


class GenericDfaService(GenericApiService):

  """Wrapper for any DFA web service."""

  # The _WRAP_LISTS constant indicates that all DFA services need to wrap lists
  # in an extra layer of XML element tags.
  _WRAP_LISTS = True
  # The _BUFFER_CLASS is the subclass of SoapBuffer that should be used to track
  # all SOAP interactions.
  _BUFFER_CLASS = DfaSoapBuffer
  # The _TOKEN_EXPIRED_ERROR_MESSAGE is returned by the DFA API when a DFA token
  # needs to be refreshed.
  _TOKEN_EXPIRED_ERROR_MESSAGE = 'Authentication token has expired.'

  def __init__(self, headers, config, op_config, lock, logger, service_name):
    """Inits GenericDfaService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: threading.RLock Thread lock to use to synchronize requests.
      logger: Logger Instance of Logger to use for logging.
      service_name: string The name of this service.
    """
    service_url = '/'.join([op_config['server'], op_config['version'],
                            'api/dfa-api', service_name])
    namespace = '/'.join(['http://www.doubleclick.net/dfa-api',
                          op_config['version']])
    namespace_extractor = _DetermineNamespacePrefix

    super(GenericDfaService, self).__init__(
        headers, config, op_config, lock, logger, service_name, service_url,
        GenericDfaService._WRAP_LISTS, GenericDfaService._BUFFER_CLASS,
        namespace, namespace_extractor)

    # DFA-specific changes to the SOAPpy.WSDL.Proxy
    methodattrs = {
        'xmlns:dfa': self._namespace
    }
    self._soappyservice.soapproxy.methodattrs = methodattrs

  def _WrapSoapCall(self, soap_call_function):
    """Gives the service a chance to wrap a call in a product-specific function.

    DFA uses this function to listen for expired DDMM tokens and refresh them.
    Calls which fail due to expired tokens will be retried.

    Args:
      soap_call_function: function The function to make a SOAP call.

    Returns:
      function A new function wrapping the input function which listens for
      token expired errors and retries the failed call.
    """

    def RefreshTokenIfExpired(*args, **kargs):
      try:
        return soap_call_function(*args, **kargs)
      except DfaAuthenticationError, e:
        if e.message == self._TOKEN_EXPIRED_ERROR_MESSAGE:
          self._GenerateToken()
          return soap_call_function(*args, **kargs)
        else:
          raise e

    return RefreshTokenIfExpired

  def _SetHeaders(self):
    """Sets the SOAP headers for this service's requests."""
    soap_headers = SOAPpy.Types.headerType()
    if self._service_name != 'login':
      if 'AuthToken' not in self._headers or not self._headers['AuthToken']:
        self._GenerateToken()
      wsse_header = SOAPpy.Types.structType(
          data={
              'UsernameToken': {
                  'Username': self._headers['Username'],
                  'Password': self._headers['AuthToken']
              }
          },
          name='Security', typed=0, attrs={'xmlns': WSSE_NS})
      soap_headers.Security = wsse_header
    request_header = SOAPpy.Types.structType(
        data={'applicationName': ''.join([self._headers['appName'], LIB_SIG])},
        name='RequestHeader', typed=0)
    soap_headers.RequestHeader = request_header
    self._soappyservice.soapproxy.header = soap_headers

  def _ReadyOAuth(self):
    """If OAuth is on, sets the transport handler to add OAuth2 HTTP header.

    DFA overrides the default implementation because only the login service
    should have this header.
    """
    if self._service_name == 'login':
      super(GenericDfaService, self)._ReadyOAuth()

  def _GetMethodInfo(self, method_name):
    """Pulls all of the relevant data about a method from a SOAPpy service.

    The return dictionary has two keys, MethodInfoKeys.INPUTS and
    MethodInfoKeys.OUTPUTS. Each of these keys has a list value. The list
    value contains a dictionary of information on each input/output parameter,
    in order.

    Args:
      method_name: string The name of the method to pull information for.

    Returns:
      dict A dictionary containing information about a SOAP method.
    """
    rval = {}
    rval[MethodInfoKeys.INPUTS] = []
    for i in range(len(self._soappyservice.methods[method_name].inparams)):
      param_attributes = self._soappyservice.methods[method_name].inparams[i]
      if hasattr(param_attributes, 'maxOccurs'):
        max_occurs = param_attributes.maxOccurs
      else:
        max_occurs = '1'
      inparam = {
          MethodInfoKeys.ELEMENT_NAME: param_attributes.name,
          MethodInfoKeys.NS: param_attributes.type[0],
          MethodInfoKeys.TYPE: param_attributes.type[1],
          MethodInfoKeys.MAX_OCCURS: max_occurs
      }
      rval[MethodInfoKeys.INPUTS].append(inparam)

    rval[MethodInfoKeys.OUTPUTS] = []
    for i in range(len(self._soappyservice.methods[method_name].outparams)):
      param_attributes = self._soappyservice.methods[method_name].outparams[i]
      if hasattr(param_attributes, 'maxOccurs'):
        max_occurs = param_attributes.maxOccurs
      else:
        max_occurs = '1'
      outparam = {
          MethodInfoKeys.ELEMENT_NAME: param_attributes.name,
          MethodInfoKeys.NS: param_attributes.type[0],
          MethodInfoKeys.TYPE: param_attributes.type[1],
          MethodInfoKeys.MAX_OCCURS: max_occurs
      }
      rval[MethodInfoKeys.OUTPUTS].append(outparam)
    return rval

  def _TakeActionOnSoapCall(self, method_name, args):
    """Gives the service a chance to take product-specific action on raw inputs.

    DFA will try to determine xsi_types for saveAd and saveCreative calls.

    Args:
      method_name: string The name of the SOAP operation being called.
      args: tuple The arguments passed into the SOAP operation.

    Returns:
      tuple The method arguments, possibly modified.
    """
    if method_name.lower() == 'savecreative':
      DfaUtils.AssignCreativeXsi(args[0])
    elif method_name.lower() == 'savead':
      DfaUtils.AssignAdXsi(args[0])
    return args

  def _ReadyCompression(self):
    """Sets whether the HTTP transport layer should use compression.

    Overloaded for DFA because the DFA servers do not accept compressed
    messages. They do support returning compressed messages.
    """
    compress = Utils.BoolTypeConvert(self._config['compress'])
    self._soappyservice.soapproxy.config.send_compressed = False
    self._soappyservice.soapproxy.config.accept_compressed = compress

  def _HandleLogsAndErrors(self, buf, start_time, stop_time, error=None):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      start_time: str Time before service call was invoked.
      stop_time: str Time after service call was invoked.
      [optional]
      error: dict Error, if any.

    Raises:
      DfaApiError: if the API calls returns a SOAP error message.
      Error: if the call returns a non-SOAP error message, such as an HTTP 502.
    """
    if error is None:
      error = {}
    try:
      handlers = self.__GetLogHandlers(buf)

      fault = super(GenericDfaService, self)._ManageSoap(
          buf, handlers, LIB_URL, start_time, stop_time, error)
      if fault:
        # Raise a specific error, subclass of DfaApiError.
        if fault['detail'] is None: del fault['detail']
        if 'detail' in fault:
          if ('google' in fault['detail'] and
              'doubleclick' not in fault['detail']):
            fault['detail']['doubleclick'] = fault['detail']['google']
          if ('doubleclick' in fault['detail'] and
              'errorCode' in fault['detail']['doubleclick']):
            code = int(fault['detail']['doubleclick']['errorCode'])
            if code == 4:
              raise DfaAuthenticationError(fault)
            else:
              raise DfaApiError(fault)
        if isinstance(fault, (str, dict)):
          raise DfaApiError(fault)
    except DfaApiError, e:
      raise e
    except Error, e:
      if error: e = error
      raise Error(e)

  def _GenerateToken(self):
    """Attempts to generate a token for the WSSE security header.

    Raises:
      DfaAuthenticationError: if there are not enough credentials to generate a
                              token or if the given credentials are invalid.
    """
    if ('Username' in self._headers and
        ('Password' in self._headers or 'oauth2credentials' in self._headers)):
      if not self._headers.get('oauth2credentials'):
        warnings.warn(_DEPRECATION_WARNING, DeprecationWarning, stacklevel=5)
      # Ensure the 'raw_response' config value is off while generating tokens.
      old_raw_response = self._config['raw_response']
      self._config['raw_response'] = 'n'
      try:
        login_service = GenericDfaService(
            self._headers, self._config, self._op_config, self._lock,
            self._logger, 'login')
        self._headers['AuthToken'] = login_service.authenticate(
            self._headers['Username'],
            self._headers.get('Password'))[0]['token']
      finally:
        self._config['raw_response'] = old_raw_response
    else:
      fault = {
          'faultstring': ('Authentication data, username/password or username/'
                          'oauth2credentials, is missing.')
      }
      raise DfaAuthenticationError(fault)

  def __GetLogHandlers(self, buf):
    """Gets a list of log handlers for the DFA library.

    Args:
      buf: SoapBuffer SOAP buffer from which calls are retrieved for logging.

    Returns:
      list Log handlers for the DFA library.
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
                        'requestID=%s'
                        % (Utils.GetNetLocFromUrl(self._service_url),
                           self._service_name, buf.GetCallName(),
                           buf.GetCallResponseTime(), buf.GetCallRequestId()))
        },
        {
            'tag': '',
            'name': 'dfa_api_lib',
            'data': ''
        }
    ]


def _DetermineNamespacePrefix(unused_url):
  """Returns the SOAP prefix to use for definitions within the given namespace.

  Args:
    unused_url: string The URL of the namespace. The DFA library doesn't
                actually check this value.

  Returns:
    string The SOAP namespace prefix to use for the given namespace. The DFA
           library always returns 'dfa:'.
  """
  return 'dfa:'
