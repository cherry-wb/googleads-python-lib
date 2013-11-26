#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""Test to cover issue 48.

Tests to make sure that if your SOAP message contains a line of asterisks 72 or
or longer in a row, the SOAP buffer can still parse it. If you have a line in
the SOAP messages containing only exactly 72 asterisks, the library will still
fail.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.common.SoapBuffer import SoapBuffer


OUTGOING_HTTP_HEADERS_BLOCK = (
    '*** Outgoing HTTP headers **********************************************\n'
    'POST /v1.19/api/dfa-api/login HTTP/1.0\n'
    'Host:advertisersapitest.doubleclick.net\n'
    'User-agent:SOAPpy 0.12.0 (pywebsvcs.sf.net),gzip\n'
    'Content-length:621\n'
    'Accept-Encoding:gzip\n'
    'SOAPAction:"authenticate"\n'
    '************************************************************************\n'
    )

OUTGOING_SOAP_BLOCK = (
    '*** Outgoing SOAP ******************************************************\n'
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<SOAP-ENV:Envelope '
    'SOAP-ENV:encodingStyle="''http://schemas.xmlsoap.org/soap/encoding/" '
    'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">\n'
    '<SOAP-ENV:Header>\n'
    '<RequestHeader>\n'
    '<MyHeader>hello soap!</applicationName>\n'
    '</RequestHeader>\n'
    '</SOAP-ENV:Header>\n'
    '<SOAP-ENV:Body>\n'
    '<dfa:authenticate xmlns:dfa="http://www.doubleclick.net/dfa-api/v1.19">\n'
    '<username>api.jdilallo</username>\n'
    '<token>\n' + ('*' * 85) +'\nxxxxx\n</token>\n'
    '</dfa:authenticate>\n'
    '</SOAP-ENV:Body>\n'
    '</SOAP-ENV:Envelope>\n'
    '************************************************************************\n'
    )

INCOMING_HTTP_HEADERS_BLOCK = (
    '*** Incoming HTTP headers **********************************************\n'
    'HTTP/1.? 200 OK\n'
    'Content-Type: text/xml; charset=utf-8\n'
    'Content-Encoding: gzip\n'
    '************************************************************************\n'
    )

INCOMING_SOAP_BLOCK = (
    '*** Incoming SOAP ******************************************************\n'
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<soapenv:Envelope '
    'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
    '<soapenv:Header>\n'
    '<ns1:ResponseHeader soapenv:mustUnderstand="0" '
    'xmlns:ns1="http://www.doubleclick.net/dfa-api/v1.19">\n'
    '<ns1:requestId>50d50367-4d13-47a0-92ab-7748da032064</ns1:requestId>\n'
    '</ns1:ResponseHeader>\n'
    '</soapenv:Header>\n'
    '<soapenv:Body>\n'
    '<ns2:authenticateResponse '
    'soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" '
    'xmlns:ns2="http://www.doubleclick.net/dfa-api/v1.19">\n'
    '<authenticateReturn href="#id0"/>\n'
    '</ns2:authenticateResponse>\n'
    '<multiRef id="id0" soapenc:root="0" '
    'soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" '
    'xmlns:ns3="http://www.doubleclick.net/dfa-api/v1.19" '
    'xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" '
    'xsi:type="ns3:UserProfile">\n'
    '<email xsi:type="soapenc:string">' + ('*' * 72) + 'test@test.com</email>\n'
    '<name xsi:type="soapenc:string">api.jdilallo</name>\n'
    '</multiRef>\n'
    '</soapenv:Body>\n'
    '</soapenv:Envelope>\n'
    '************************************************************************\n'
    )


class SoapBufferTest(unittest.TestCase):

  """Tests for the adspygoogle.common.SoapBuffer module."""

  def testIssue48Regression(self):
    """Regression test for issue 48 on the issue tracker."""
    buf = SoapBuffer()
    buf.write(OUTGOING_HTTP_HEADERS_BLOCK)
    buf.write(OUTGOING_SOAP_BLOCK)
    buf.write(INCOMING_HTTP_HEADERS_BLOCK)
    buf.write(INCOMING_SOAP_BLOCK)

    self.assertEqual(OUTGOING_HTTP_HEADERS_BLOCK.strip(), buf.GetHeadersOut())
    self.assertEqual(OUTGOING_SOAP_BLOCK.strip(), buf.GetSoapOut())
    self.assertEqual(INCOMING_HTTP_HEADERS_BLOCK.strip(), buf.GetHeadersIn())
    self.assertEqual(INCOMING_SOAP_BLOCK.strip(), buf.GetSoapIn())


if __name__ == '__main__':
  unittest.main()
