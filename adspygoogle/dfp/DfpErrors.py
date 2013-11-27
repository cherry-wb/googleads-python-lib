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

"""Classes for handling errors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.Errors import DetailError
from adspygoogle.common.Errors import Error
from adspygoogle.dfp import ERROR_TYPES


class DfpError(Error):

  """Implements DfpError.

  Responsible for handling error.
  """

  def __init(self, msg):
    super(DfpError, self).__init__()

  def __str__(self):
    return super(DfpError, self).__str__()

  def __call__(self):
    return super(DfpError, self).__call__()


class DfpDetailError(DetailError):

  """Implements DfpDetailError.

  Responsible for handling detailed ApiException error.
  """

  def __init__(self, **error):
    super(DfpDetailError, self).__init__()
    self.__error = error
    for key in self.__error:
      self.__dict__.__setitem__(key, self.__error[key])

  def __call__(self):
    return (self.__error,)


class DfpApiError(DfpError):

  """Implements DfpApiError.

  Responsible for handling API exception.
  """

  def __init__(self, fault):
    (self.__fault, self.fault_code, self.fault_string) = (fault, '', '')
    if 'faultcode' in fault: self.fault_code = fault['faultcode']
    if 'faultstring' in fault: self.fault_string = fault['faultstring']

    (self.message, self.trigger, self.errors) = ('', '', [])
    if 'detail' in fault:
      if 'message' in fault['detail']: self.message = fault['detail']['message']
    if not self.message: self.message = self.fault_string

    errors = [None]
    if 'detail' in fault and 'errors' in fault['detail']:
      errors = fault['detail']['errors']
    elif 'detail' not in fault:
      errors[0] = {}
    else:
      errors[0] = fault['detail']
    if isinstance(errors, list):
      for error in errors:
        # Keys need to be of type str not unicode.
        error_dct = dict([(str(key), value) for key, value in error.items()])
        self.errors.append(DfpDetailError(**error_dct))
    else:
      # Keys need to be of type str not unicode.
      error_dct = dict([(str(key), value) for key, value in errors.items()])
      self.errors.append(DfpDetailError(**error_dct))

  def __str__(self):
    return self.fault_string

  def __call__(self):
    return (self.__fault,)


class DfpRequestError(DfpApiError):

  """Implements DfpRequestError.

  Responsible for handling request error."""

  pass


class DfpGoogleInternalError(DfpApiError):

  """Implements DfpGoogleInternalError.

  Responsible for handling Google internal error.
  """

  pass


class DfpAuthenticationError(DfpApiError):

  """Implements DfpAuthenticationError.

  Responsible for handling authentication error.
  """

  pass


class DfpAccountError(DfpApiError):

  """Implements DfpAccountError.

  Responsible for handling account error.
  """

  pass


class DfpWebpageError(DfpApiError):

  """Implements DfpWebpageError.

  Responsible for handling webpage error.
  """

  pass


class DfpBillingError(DfpApiError):

  """Implements DfpBillingError.

  Responsible for handling billing error.
  """

  pass


# Map error codes and types to their corresponding classes.
ERRORS = {}
for index in ERROR_TYPES:
  if index in ('AdUnitAfcSizeError', 'AdUnitCodeError', 'AdUnitHierarchyError',
               'ApiError', 'ApiVersionError', 'CommonError', 'CreativeError',
               'CustomTargetingError', 'DayPartTargetingError', 'FileError',
               'FlashCreativeError', 'ForecastError', 'GeoTargetingError',
               'ImageError', 'InvalidUrlError', 'InventoryTargetingError',
               'InventoryUnitError', 'LineItemCreativeAssociationError',
               'LineItemCreativeAssociationOperationError',
               'LineItemFlightDateError', 'LineItemOperationError',
               'NotNullError', 'NullError', 'OrderActionError', 'OrderError',
               'ParseError', 'PermissionError',
               'PublisherQueryLanguageContextError',
               'PublisherQueryLanguageSyntaxError', 'RangeError', 'RegExError',
               'RequiredCollectionError', 'RequiredError',
               'RequiredNumberError', 'RequiredSizeError', 'ReportError',
               'ReservationDetailsError', 'StatementError', 'StringLengthError',
               'TypeError', 'UniqueError', 'UserDomainTargetingError'):
    ERRORS[index] = DfpRequestError
  elif index in ('InternalApiError', 'QuotaError', 'ServerError'):
    ERRORS[index] = DfpGoogleInternalError
  elif index in ('AuthenticationError', 'InvalidEmailError'):
    ERRORS[index] = DfpAuthenticationError
