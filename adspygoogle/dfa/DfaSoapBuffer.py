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

"""Handler class for implementing a SOAP buffer."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.SoapBuffer import SoapBuffer


class DfaSoapBuffer(SoapBuffer):

  """Implements a DfaSoapBuffer.

  Catches and parses outgoing and incoming SOAP XML messages for DFA API
  requests.
  """

  def __init__(self, xml_parser=None, pretty_xml=False):
    """Inits DfaSoapBuffer.

    Args:
      xml_parser: str XML parser to use.
      pretty_xml: bool Indicator for whether to prettify XML.
    """
    super(DfaSoapBuffer, self).__init__(xml_parser, pretty_xml)
    self.__xml_parser = xml_parser

  def __GetXmlOut(self):
    """Remove banners from outgoing SOAP XML and contstruct XML object.

    Returns:
      Document/Element Object generated from string, representing XML message.
    """
    return super(DfaSoapBuffer, self)._GetXmlOut()

  def __GetXmlIn(self):
    """Remove banners from incoming SOAP XML and construct XML object.

    Returns:
      Document/Element Object generated from string, representing XML message.
    """
    return super(DfaSoapBuffer, self)._GetXmlIn()

  def __GetXmlValueByName(self, xml_obj, names, get_all=False):
    """Get XML object value from a given tag name.

    Args:
      xml_obj: Document/Element object.
      names: list List of tag names whose value to look up.
      get_all: bool Whether to return all values that were found or just one.

    Returns:
      str XML object value, list if more than one value is found and if
      explicitly requested, or None if name is not found in the XML object.
    """
    response = None
    for name in names:
      response = super(DfaSoapBuffer, self)._GetXmlValueByName(
          xml_obj, name, get_all)
      if response: break
    return response

  def GetCallResponseTime(self):
    """Get value for responseTime header.

    Returns:
      str responseTime header value.
    """
    return self.__GetXmlValueByName(
        self._GetXmlIn(), ['responseTime', 'Header/ResponseHeader/responseTime',
                           'ns1:responseTime'])

  def GetCallRequestId(self):
    """Get value for requestId header.

    Returns:
      str requestId header value.
    """
    return self.__GetXmlValueByName(
        self._GetXmlIn(), ['requestId', 'Header/ResponseHeader/requestId',
                           'ns1:requestId'])
