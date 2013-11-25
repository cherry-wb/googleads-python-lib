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
import threading

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Client import Client
from adspygoogle.common.Logger import Logger
from adspygoogle.dfa import DEFAULT_API_VERSION
from adspygoogle.dfa import DfaSanityCheck
from adspygoogle.dfa import DfaUtils
from adspygoogle.dfa import LIB_SIG
from adspygoogle.dfa import REQUIRED_SOAP_HEADERS
from adspygoogle.dfa.GenericDfaService import GenericDfaService


class DfaClient(Client):

  """Provides entry point to all web services.

  Allows instantiation of all DFA API web services.
  """

  auth_pkl_name = 'dfa_api_auth.pkl'
  config_pkl_name = 'dfa_api_config.pkl'

  def __init__(self, headers=None, config=None, path=None):
    """Inits DfaClient.

    Args:
      [optional]
      headers: dict Object with populated authentication credentials.
      config: dict Object with client configuration values.
      path: str Relative or absolute path to home directory (i.e. location of
            pickles and logs/).

    Example:
      headers = {
        'Username': 'johndoe@example.com',
        'Password': 'secret',
        'AuthToken': '...'
      }
      config = {
        'home': '/path/to/home',
        'log_home': '/path/to/logs/home',
        'xml_parser': '1', # PYXML = 1, ELEMENTREE = 2
        'debug': 'n',
        'raw_debug': 'n',
        'xml_log': 'y',
        'request_log': 'y',
        'raw_response': 'n',
        'strict': 'y',
        'pretty_xml': 'y',
        'compress': 'y',
      }
      path = '/path/to/home'
    """
    super(DfaClient, self).__init__(headers, config, path)

    self.__lock = threading.RLock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of DfaClient, based on
      # provided relative path.
      if os.path.isabs(path):
        DfaClient.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to DfaClient.home. Otherwise, may break when
        # multiple instances of DfaClient exist during program run.
        DfaClient.home = os.path.join(os.getcwd(), path)

      # If pickles don't exist at given location, default to "~".
      if (not headers and not config and
          (not os.path.exists(os.path.join(DfaClient.home,
                                           DfaClient.auth_pkl_name)) or
           not os.path.exists(os.path.join(DfaClient.home,
                                           DfaClient.config_pkl_name)))):
        DfaClient.home = os.path.expanduser('~')
    else:
      DfaClient.home = os.path.expanduser('~')

    # Update location for both pickles.
    DfaClient.auth_pkl = os.path.join(DfaClient.home,
                                      DfaClient.auth_pkl_name)
    DfaClient.config_pkl = os.path.join(DfaClient.home,
                                        DfaClient.config_pkl_name)

    # Only load from the pickle if config wasn't specified.
    self._config = config or self.__LoadConfigValues()
    self._config = self.__SetMissingDefaultConfigValues(self._config)
    self._config['home'] = DfaClient.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self._config['xml_parser'])

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self._headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self._config['strict']):
        SanityCheck.ValidateRequiredHeaders(headers, REQUIRED_SOAP_HEADERS)
      self._headers = headers

    # Initialize logger.
    self.__logger = Logger(LIB_SIG, self._config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from dfa_api_auth.pkl.

    Returns:
      dict Dictionary object with populated authentication credentials.
    """
    return super(DfaClient, self)._LoadAuthCredentials()

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in dfa_api_auth.pkl.

    Args:
      key: str Key to update.
      new_value: str New value to update the key with.
    """
    super(DfaClient, self)._WriteUpdatedAuthValue(key, new_value)

  def __LoadConfigValues(self):
    """Load existing configuration values from dfa_api_config.pkl.

    Returns:
      dict Dictionary object with populated configuration values.
    """
    return super(DfaClient, self)._LoadConfigValues()

  def __SetMissingDefaultConfigValues(self, config=None):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict Object with client configuration values.

    Returns:
      dictionary Configuration values with defaults added in.
    """
    if config is None:
      config = {}
    config = super(DfaClient, self)._SetMissingDefaultConfigValues(config)

    default_config = {
        'home': DfaClient.home,
        'log_home': os.path.join(DfaClient.home, 'logs')
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
    service_name = DfaUtils.DetermineServiceFromUrl(url).capitalize()
    service = getattr(self, 'Get' + service_name + 'Service')(
        server=server, http_proxy=http_proxy)

    return service.CallRawMethod(soap_message)

  def GetService(self, service_name,
                 server='https://advertisersapi.doubleclick.net', version=None,
                 http_proxy=None, op_config=None):
    """Generic method to create a service.

    Args:
      service_name: str Name of the service to create.
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    if op_config is None:
      op_config = {
          'server': server,
          'version': version,
          'http_proxy': http_proxy
      }
    return GenericDfaService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, service_name)

  def GetAdService(self, server='https://advertisersapi.doubleclick.net',
                   version=None, http_proxy=None):
    """Returns an object which can call methods in the ad service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('ad', server, version, http_proxy)

  def GetAdvertiserService(self,
                           server='https://advertisersapi.doubleclick.net',
                           version=None, http_proxy=None):
    """Returns an object which can call methods in the advertiser service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('advertiser', server, version, http_proxy)

  def GetAdvertiserGroupService(self,
                                server='https://advertisersapi.doubleclick.net',
                                version=None, http_proxy=None):
    """Returns an object which can call methods in the advertisergroup service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('advertisergroup', server, version, http_proxy)

  def GetCampaignService(self, server='https://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Returns an object which can call methods in the campaign service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('campaign', server, version, http_proxy)

  def GetChangeLogService(self, server='https://advertisersapi.doubleclick.net',
                          version=None, http_proxy=None):
    """Returns an object which can call methods in the changelog service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('changelog', server, version, http_proxy)

  def GetContentCategoryService(self,
                                server='https://advertisersapi.doubleclick.net',
                                version=None, http_proxy=None):
    """Returns an object which can call methods in the contentcategory service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('contentcategory', server, version, http_proxy)

  def GetCreativeService(self, server='https://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Returns an object which can call methods in the creative service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('creative', server, version, http_proxy)

  def GetCreativeFieldService(self,
                              server='https://advertisersapi.doubleclick.net',
                              version=None, http_proxy=None):
    """Returns an object which can call methods in the creativefield service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('creativefield', server, version, http_proxy)

  def GetCreativeGroupService(self,
                              server='https://advertisersapi.doubleclick.net',
                              version=None, http_proxy=None):
    """Returns an object which can call methods in the creativegroup service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('creativegroup', server, version, http_proxy)

  def GetLoginService(self, server='https://advertisersapi.doubleclick.net',
                      version=None, http_proxy=None):
    """Returns an object which can call methods in the login service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('login', server, version, http_proxy)

  def GetNetworkService(self, server='https://advertisersapi.doubleclick.net',
                        version=None, http_proxy=None):
    """Returns an object which can call methods in the network service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('network', server, version, http_proxy)

  def GetPlacementService(self, server='https://advertisersapi.doubleclick.net',
                          version=None, http_proxy=None):
    """Returns an object which can call methods in the placement service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('placement', server, version, http_proxy)

  def GetReportService(self, server='https://advertisersapi.doubleclick.net',
                       version=None, http_proxy=None):
    """Returns an object which can call methods in the report service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('report', server, version, http_proxy)

  def GetSiteService(self, server='https://advertisersapi.doubleclick.net',
                     version=None, http_proxy=None):
    """Returns an object which can call methods in the site service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('site', server, version, http_proxy)

  def GetSizeService(self, server='https://advertisersapi.doubleclick.net',
                     version=None, http_proxy=None):
    """Returns an object which can call methods in the size service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('size', server, version, http_proxy)

  def GetSpotlightService(self, server='https://advertisersapi.doubleclick.net',
                          version=None, http_proxy=None):
    """Returns an object which can call methods in the spotlight service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('spotlight', server, version, http_proxy)

  def GetStrategyService(self, server='https://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Returns an object which can call methods in the strategy service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('strategy', server, version, http_proxy)

  def GetSubnetworkService(self,
                           server='https://advertisersapi.doubleclick.net',
                           version=None, http_proxy=None):
    """Returns an object which can call methods in the subnetwork service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('subnetwork', server, version, http_proxy)

  def GetUserService(self, server='https://advertisersapi.doubleclick.net',
                     version=None, http_proxy=None):
    """Returns an object which can call methods in the user service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('user', server, version, http_proxy)

  def GetUserRoleService(self, server='https://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Returns an object which can call methods in the userrole service.

    Args:
      [optional]
      server: str API server this object will access. Possible values are:
              'https://advertisersapi.doubleclick.net' for production,
              'https://advertisersapitest.doubleclick.net' for test, and
              'https://betaadvertisersapi.doubleclick.net' for beta.
              The default behavior is to access the production environment.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfaService New object representing the SOAP service.
    """
    return self.GetService('userrole', server, version, http_proxy)
