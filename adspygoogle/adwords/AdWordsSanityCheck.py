#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.Errors import ValidationError

DEPRECATED_AFTER = {
    'UserListService': 'v201306',
    'AdExtensionOverrideService': 'v201306'
}

# A map of the supported servers for each version.
_VERSION_SERVER_MAP = {
    'v201306': ('https://adwords.google.com',),
    'v201309': ('https://adwords.google.com',),
}


def ValidateServer(server, version):
  """Sanity check for API server.

  Args:
    server: str API server to access for this API call.
    version: str API version being used to access the server.

  Raises:
    ValidationError: if the given API server or version is not valid.
  """
  if version not in _VERSION_SERVER_MAP:
    raise ValidationError(
        'Given API version, \'%s\', is not valid. Expecting one of %s.'
        % (version, sorted(_VERSION_SERVER_MAP.keys())))

  if server not in _VERSION_SERVER_MAP[version]:
    raise ValidationError(
        'Given API server, \'%s\', is not a valid server for version \'%s\'. '
        'Expecting one of %s.'
        % (server, version, sorted(_VERSION_SERVER_MAP[version])))


def ValidateService(service, version):
  """Checks if this service is available in the requested version.

  Args:
    service: str Service being requested.
    version: str Version being requested.
  """
  if service in DEPRECATED_AFTER and version > DEPRECATED_AFTER[service]:
    raise ValidationError('%s is not available in %s' % (service, version))
