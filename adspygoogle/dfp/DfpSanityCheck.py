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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.Errors import ValidationError


def ValidateServer(server, version):
  """Sanity check for API server.

  Args:
    server: str API server to access for this API call.
    version: str API version being used to access the server.

  Raises:
    ValidationError: if the given API server or version is not valid.
  """
  # Map of supported API servers and versions.
  servers = {'v201208': 'https://www.google.com',
             'v201211': 'https://www.google.com',
             'v201302': 'https://www.google.com',
             'v201306': 'https://www.google.com',
             'v201308': 'https://www.google.com',
             'v201311': 'https://www.google.com'}

  if server not in servers.values():
    msg = ('Given API server, \'%s\', is not valid. Expecting '
           '\'https://www.google.com\'.' % server)
    raise ValidationError(msg)

  if version not in servers.keys():
    msg = ('Given API version, \'%s\', is not valid. Expecting one of %s.'
           % (version, sorted(set(servers.keys()))))
    raise ValidationError(msg)

  if server != servers[version]:
    msg = ('Given API version, \'%s\', is not compatible with given server, '
           '\'%s\'.' % (version, server))
    raise ValidationError(msg)
