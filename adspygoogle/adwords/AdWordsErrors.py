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


class AdWordsError(Error):

  """Implements AdWordsError.

  Responsible for handling error.
  """
  pass


class AdWordsDetailError(DetailError):

  """Implements AdWordsDetailError.

  Responsible for handling detailed ApiException error.
  """

  def __init__(self, **error):
    DetailError.__init__(self)
    self.__error = error
    for key in self.__error:
      self.__dict__.__setitem__(key, self.__error[key])

  def __call__(self):
    return (self.__error,)


class AdWordsApiError(AdWordsError):

  """Implements AdWordsApiError.

  Responsible for handling API exception.
  """

  def __init__(self, fault):
    (self.__fault, self.fault_code, self.fault_string) = (fault, '', '')
    if 'faultcode' in fault: self.fault_code = fault['faultcode']
    if 'faultstring' in fault: self.fault_string = fault['faultstring']

    (self.code, error_msg, self.trigger, self.errors) = (-1, '', '', [])
    if 'detail' in fault and fault['detail']:
      if 'code' in fault['detail']: self.code = int(fault['detail']['code'])
      if 'trigger' in fault['detail']: self.trigger = fault['detail']['trigger']
      if 'message' in fault['detail']: error_msg = fault['detail']['message']
    if not error_msg: error_msg = self.fault_string

    errors = [None]
    if 'detail' in fault and fault['detail'] and 'errors' in fault['detail']:
      errors = fault['detail']['errors']
    elif 'detail' not in fault or not fault['detail']:
      errors[0] = {}
    else:
      errors[0] = fault['detail']
    if isinstance(errors, list):
      for error in errors:
        # Keys need to be of type str not unicode.
        error_dct = dict([(str(key), value) for key, value in error.items()])
        self.errors.append(AdWordsDetailError(**error_dct))
    else:
      # Keys need to be of type str not unicode.
      error_dct = dict([(str(key), value) for key, value in errors.items()])
      self.errors.append(AdWordsDetailError(**error_dct))
    AdWordsError.__init__(self, error_msg)

  def __call__(self):
    return (self.__fault,)


class AdWordsRequestError(AdWordsApiError):

  """Implements AdWordsRequestError.

  Responsible for handling request error."""

  pass


class AdWordsGoogleInternalError(AdWordsApiError):

  """Implements AdWordsGoogleInternalError.

  Responsible for handling Google internal error.
  """

  pass


class AdWordsAuthenticationError(AdWordsApiError):

  """Implements AdWordsAuthenticationError.

  Responsible for handling authentication error.
  """

  pass


class AdWordsAccountError(AdWordsApiError):

  """Implements AdWordsAccountError.

  Responsible for handling account error.
  """

  pass


class AdWordsWebpageError(AdWordsApiError):

  """Implements AdWordsWebpageError.

  Responsible for handling webpage error.
  """

  pass


class AdWordsBillingError(AdWordsApiError):

  """Implements AdWordsBillingError.

  Responsible for handling billing error.
  """

  pass


class AdWordsReportError(AdWordsError):

  def __init__(self, http_code, error_type, trigger, field_path):
    self.http_code = http_code
    self.type = error_type
    self.trigger = trigger
    self.field_path = field_path
    message = ('HTTP code: %s, type: \'%s\', trigger: \'%s\', '
               'field path: \'%s\'' %
               (http_code, error_type, trigger, field_path))
    super(AdWordsReportError, self).__init__(message)


# Map error codes and types to their corresponding classes.
ERRORS = {}
for e_type in ('AdError', 'AdExtensionError', 'AdExtensionOverrideError',
               'AdGroupAdError', 'AdGroupCriterionError',
               'AdGroupServiceError', 'AdParamError', 'AdParamPolicyError',
               'AlertError', 'ApiError', 'ApiUsageError', 'AudioError',
               'BidLandscapeServiceError', 'BiddingError',
               'BiddingTransitionError', 'BudgetError', 'BulkMutateJobError',
               'CampaignAdExtensionError',
               'CampaignCriterionError', 'CampaignError',
               'CollectionSizeError', 'ConversionTrackingError',
               'CriterionError', 'CriterionPolicyError', 'CurrencyCodeError',
               'CustomerSyncError', 'DataError', 'DateError', 'DistinctError',
               'ExperimentServiceError', 'GeoLocationError', 'IdError',
               'ImageError', 'JobError', 'MatchesRegexError', 'MediaError',
               'NewEntityCreationError', 'NotEmptyError', 'NullError',
               'OperatorError', 'OpportunityError', 'PagingError',
               'PolicyViolationError', 'RangeError', 'ReadOnlyError',
               'RegionCodeError', 'RejectedError', 'ReportDefinitionError',
               'RequestError', 'RequiredError', 'SelectorError',
               'ServicedAccountError', 'SettingError', 'SizeLimitError',
               'StatsQueryError', 'StringLengthError', 'TargetError',
               'TargetingIdeaError', 'TrafficEstimatorError', 'UserListError',
               'VideoError'):
  ERRORS[e_type] = AdWordsRequestError
for e_type in ('InternalApiError', 'DatabaseError', 'QuotaCheckError',
               'QuotaError', 'QuotaExceededError', 'RateExceededError'):
  ERRORS[e_type] = AdWordsGoogleInternalError
for e_type in ('ClientTermsError', 'NotWhitelistedError'):
  ERRORS[e_type] = AdWordsAccountError
for e_type in ('AuthenticationError', 'AuthorizationError'):
  ERRORS[e_type] = AdWordsAuthenticationError
