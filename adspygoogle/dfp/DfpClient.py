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

"""Interface for accessing all other services."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import re
import thread
import time

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Client import Client
from adspygoogle.common.Errors import AuthTokenError
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.Logger import Logger
from adspygoogle.dfp import AUTH_TOKEN_SERVICE
from adspygoogle.dfp import DEFAULT_API_VERSION
from adspygoogle.dfp import DfpSanityCheck
from adspygoogle.dfp import LIB_SHORT_NAME
from adspygoogle.dfp import LIB_SIG
from adspygoogle.dfp import REQUIRED_SOAP_HEADERS
from adspygoogle.dfp.GenericDfpService import GenericDfpService


class DfpClient(Client):

  """Provides entry point to all web services.

  Allows instantiation of all DFP API web services.
  """

  auth_pkl_name = 'dfp_api_auth.pkl'
  config_pkl_name = 'dfp_api_config.pkl'

  def __init__(self, headers=None, config=None, path=None):
    """Inits Client.

    Args:
      [optional]
      headers: dict Object with populated authentication credentials.
      config: dict Object with client configuration values.
      path: str Relative or absolute path to home directory (i.e. location of
            pickles and logs/).

    Example:
      headers = {
        'email': 'johndoe@example.com',
        'password': 'secret',
        'authToken': '...',
        'applicationName': 'GoogleTest',
        'networkCode': 'ca-01234567',
        'oauth2credentials': 'See use_oauth2.py'
      }
      config = {
        'home': '/path/to/home',
        'log_home': '/path/to/logs/home',
        'proxy': 'http://example.com:8080',
        'xml_parser': '1', # PYXML = 1, ELEMENTREE = 2
        'debug': 'n',
        'raw_debug': 'n',
        'xml_log': 'y',
        'request_log': 'y',
        'raw_response': 'n',
        'strict': 'y',
        'pretty_xml': 'y',
        'compress': 'y',
        'access': ''
      }
      path = '/path/to/home'
    """
    super(DfpClient, self).__init__(headers, config, path)

    self.__lock = thread.allocate_lock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of DfpClient, based on
      # provided relative path.
      if os.path.isabs(path):
        DfpClient.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to DfpClient.home. Otherwise, may break when
        # multiple instances of DfpClient exist during program run.
        DfpClient.home = os.path.join(os.getcwd(), path)

      # If pickles don't exist at given location, default to "~".
      if (not headers and not config and
          (not os.path.exists(os.path.join(DfpClient.home,
                                           DfpClient.auth_pkl_name)) or
           not os.path.exists(os.path.join(DfpClient.home,
                                           DfpClient.config_pkl_name)))):
        DfpClient.home = os.path.expanduser('~')
    else:
      DfpClient.home = os.path.expanduser('~')

    # Update location for both pickles.
    DfpClient.auth_pkl = os.path.join(DfpClient.home,
                                      DfpClient.auth_pkl_name)
    DfpClient.config_pkl = os.path.join(DfpClient.home,
                                        DfpClient.config_pkl_name)

    # Only load from the pickle if config wasn't specified.
    self._config = config or self.__LoadConfigValues()
    self._config = self.__SetMissingDefaultConfigValues(self._config)
    self._config['home'] = DfpClient.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self._config['xml_parser'])

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self._headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self._config['strict']):
        SanityCheck.ValidateRequiredHeaders(headers, REQUIRED_SOAP_HEADERS)
      self._headers = headers

    # Load/set authentication token.
    try:
      if headers and 'authToken' in headers and headers['authToken']:
        self._headers['authToken'] = headers['authToken']
      elif 'email' in self._headers and 'password' in self._headers:
        self._headers['authToken'] = Utils.GetAuthToken(
            self._headers['email'], self._headers['password'],
            AUTH_TOKEN_SERVICE, LIB_SIG, self._config['proxy'])
      elif (self._headers.get('oauth2credentials')):
        # If they have oauth2credentials, that's also fine.
        pass
      else:
        msg = ('Authentication data, email or/and password, OAuth2 credentials '
               'is missing.')
        raise ValidationError(msg)
      self._config['auth_token_epoch'] = time.time()
    except AuthTokenError:
      # We would end up here if non-valid Google Account's credentials were
      # specified.
      self._headers['authToken'] = None
      self._config['auth_token_epoch'] = 0

    # Insert library's signature into application name.
    if self._headers['applicationName'].rfind(LIB_SIG) == -1:
      # Make sure library name shows up only once.
      if self._headers['applicationName'].rfind(LIB_SHORT_NAME) > -1:
        pattern = re.compile('.*' + LIB_SHORT_NAME + '.*?\|')
        self._headers['applicationName'] = pattern.sub(
            '', self._headers['applicationName'], 1)
      self._headers['applicationName'] = (
          '%s%s' % (self._headers['applicationName'], LIB_SIG))

    # Initialize logger.
    self.__logger = Logger(LIB_SIG, self._config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from dfp_api_auth.pkl.

    Returns:
      dict Dictionary object with populated authentication credentials.
    """
    return super(DfpClient, self)._LoadAuthCredentials()

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in dfp_api_auth.pkl.

    Args:
      key: str Key to update.
      new_value: str New value to update the key with.
    """
    super(DfpClient, self)._WriteUpdatedAuthValue(key, new_value)

  def __LoadConfigValues(self):
    """Load existing configuration values from dfp_api_config.pkl.

    Returns:
      dict Dictionary object with populated configuration values.
    """
    return super(DfpClient, self)._LoadConfigValues()

  def __SetMissingDefaultConfigValues(self, config=None):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict Object with client configuration values.

    Returns:
      dict The config dictionary with default values added.
    """
    if config is None: config = {}
    config = super(DfpClient, self)._SetMissingDefaultConfigValues(config)
    default_config = {
        'home': DfpClient.home,
        'log_home': os.path.join(DfpClient.home, 'logs')
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]
    return config

  def CallRawMethod(self, soap_message, url, server, http_proxy):
    """Call API method directly, using raw SOAP message.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      soap_message: str SOAP XML message.
      url: str URL of the API service for the method to call.
      server: str API server to access for this API call.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple Response from the API method (SOAP XML response message).
    """
    service_name = url.split('/')[-1]
    service = getattr(self, 'Get' + service_name)(server=server,
                                                  http_proxy=http_proxy)
    return service.CallRawMethod(soap_message)

  def GetService(self, service_name, server='https://www.google.com',
                 version=None, http_proxy=None, op_config=None):
    """Generic method to create a service.

    Args:
      service_name: str Name of the service to create.
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.
      op_config: dict service configuration.

    Returns:
      GenericDfpService New object representing the SOAP service.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    if op_config is None:
      op_config = {
          'server': server,
          'version': version,
          'http_proxy': http_proxy
      }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, service_name)

  def GetCompanyService(self, server='https://www.google.com', version=None,
                        http_proxy=None):
    """Create a CompanyService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the CompanyService object.
    """
    return self.GetService('CompanyService', server, version, http_proxy)

  def GetContentService(self, server='https://www.google.com', version=None,
                        http_proxy=None):
    """Create a ContentService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ContentService object.
    """
    return self.GetService('ContentService', server, version, http_proxy)

  def GetCreativeService(self, server='https://www.google.com',
                         version=None, http_proxy=None):
    """Create a CreativeService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the CreativeService
      object.
    """
    return self.GetService('CreativeService', server, version, http_proxy)

  def GetCreativeTemplateService(self, server='https://www.google.com',
                                 version=None, http_proxy=None):
    """Create a CreativeTemplateService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the CreativeTemplateService
      object.
    """
    return self.GetService('CreativeTemplateService', server, version,
                           http_proxy)

  def GetCustomTargetingService(self, server='https://www.google.com',
                                version=None, http_proxy=None):
    """Create a CustomTargetingService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the CustomTargetingService
      object.
    """
    return self.GetService('CustomTargetingService', server, version,
                           http_proxy)

  def GetForecastService(self, server='https://www.google.com',
                         version=None, http_proxy=None):
    """Create a ForecastService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ForecastService object.
    """
    return self.GetService('ForecastService', server, version, http_proxy)

  def GetInventoryService(self, server='https://www.google.com',
                          version=None, http_proxy=None):
    """Create a InventoryService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the InventoryService object.
    """
    return self.GetService('InventoryService', server, version, http_proxy)

  def GetLabelService(self, server='https://www.google.com',
                      version=None, http_proxy=None):
    """Create a LabelService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the LabelService object.
    """
    return self.GetService('LabelService', server, version, http_proxy)

  def GetLineItemCreativeAssociationService(self,
                                            server='https://www.google.com',
                                            version=None, http_proxy=None):
    """Create a LineItemCreativeAssociationService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the
      LineItemCreativeAssociationService object.
    """
    return self.GetService('LineItemCreativeAssociationService', server,
                           version, http_proxy)

  def GetLineItemService(self, server='https://www.google.com',
                         version=None, http_proxy=None):
    """Create a LineItemService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the LineItemService object.
    """
    return self.GetService('LineItemService', server, version, http_proxy)

  def GetNetworkService(self, server='https://www.google.com', version=None,
                        http_proxy=None):
    """Create a NetworkService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the NetworkService object.
    """
    return self.GetService('NetworkService', server, version, http_proxy)

  def GetOrderService(self, server='https://www.google.com', version=None,
                      http_proxy=None):
    """Create a OrderService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the OrderService object.
    """
    return self.GetService('OrderService', server, version, http_proxy)

  def GetPlacementService(self, server='https://www.google.com',
                          version=None, http_proxy=None):
    """Create a PlacementService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the PlacementService object.
    """
    return self.GetService('PlacementService', server, version, http_proxy)

  def GetPublisherQueryLanguageService(self,
                                       server='https://www.google.com',
                                       version=None, http_proxy=None):
    """Create a PublisherQueryLanguageService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the
      PublisherQueryLanguageService object.
    """
    return self.GetService('PublisherQueryLanguageService', server, version,
                           http_proxy)

  def GetReportService(self, server='https://www.google.com',
                       version=None, http_proxy=None):
    """Create a ReportService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ReportService object.
    """
    return self.GetService('ReportService', server, version, http_proxy)

  def GetSuggestedAdUnitService(self, server='https://www.google.com',
                                version=None, http_proxy=None):
    """Create a SuggestedAdUnitService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the SuggestedAdUnitService
      object.
    """
    return self.GetService('SuggestedAdUnitService', server, version,
                           http_proxy)

  def GetThirdPartySlotService(self, server='https://www.google.com',
                               version=None, http_proxy=None):
    """Create a ThirdPartySlotService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ThirdPartySlotService
      object.
    """
    return self.GetService('ThirdPartySlotService', server, version, http_proxy)

  def GetUserService(self, server='https://www.google.com', version=None,
                     http_proxy=None):
    """Create a UserService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the UserService object.
    """
    return self.GetService('UserService', server, version, http_proxy)

  def GetActivityService(self, server='https://www.google.com', version=None,
                         http_proxy=None):
    """Create an ActivityService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ActivityService object.
    """
    return self.GetService('ActivityService', server, version, http_proxy)

  def GetActivityGroupService(self, server='https://www.google.com',
                              version=None, http_proxy=None):
    """Create an ActivityGroupService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ActivityGroupService object.
    """
    return self.GetService('ActivityGroupService', server, version, http_proxy)

  def GetAdRuleService(self, server='https://www.google.com', version=None,
                       http_proxy=None):
    """Create an AdRuleService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the AdRuleService object.
    """
    return self.GetService('AdRuleService', server, version, http_proxy)

  def GetContentBundleService(self, server='https://www.google.com',
                              version=None, http_proxy=None):
    """Create an ContentBundleService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ContentBundleService object.
    """
    return self.GetService('ContentBundleService', server, version, http_proxy)

  def GetContactService(self, server='https://www.google.com',
                        version=None, http_proxy=None):
    """Create an ContactService.

    Args:
      [optional]
      server: str API server to access for API calls. The default value is
              'https://www.google.com'.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New object representing the ContactService object.
    """
    return self.GetService('ContactService', server, version, http_proxy)
