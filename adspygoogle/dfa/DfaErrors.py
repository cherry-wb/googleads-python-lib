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

"""Classes for handling errors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.Errors import Error


class DfaError(Error):

  """Implements a DfaError, responsible for wrapping errors."""

  pass


class DfaApiError(DfaError):

  """Implements a DfaApiError, responsible for handling API exception."""

  def __init__(self, fault):
    (self.__fault, self.fault_code, self.fault_string) = (fault, '', '')
    if 'faultcode' in fault: self.fault_code = fault['faultcode']
    if 'faultstring' in fault: self.fault_string = fault['faultstring']

    (self.code, self.error_message, self.localized_message, self.message,
     self.hostname) = (-1, '', '', '', '')
    if 'detail' in fault and 'doubleclick' in fault['detail']:
      if 'errorCode' in fault['detail']['doubleclick']:
        self.code = int(fault['detail']['doubleclick']['errorCode'])
      if 'errorMessage' in fault['detail']['doubleclick']:
        self.error_message = fault['detail']['doubleclick']['errorMessage']
      if 'localizedMessage' in fault['detail']['doubleclick']:
        self.localized_message = fault['detail']['doubleclick'][
            'localizedMessage']
      if 'message' in fault['detail']['doubleclick']:
        self.message = fault['detail']['doubleclick']['message']
      if 'hostname' in fault['detail']:
        self.hostname = fault['detail']['hostname']
    if not self.message: self.message = self.fault_string

  def __str__(self):
    if self.code > -1:
      return 'Code %s: %s' % (self.code, self.message)
    else:
      return self.fault_string

  def __call__(self):
    return (self.__fault,)


class DfaAuthenticationError(DfaApiError):

  """Implements DfaAuthenticationError.

  Responsible for handling authentication error.
  """

  pass
