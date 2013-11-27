#The Google Ads APIs Python Client Libraries


This client library simplifies accessing Google's SOAP Ads APIs - AdWords, 
DoubleClick Ad Exchange SOAP, DoubleClick for Advertisers, and DoubleClick for 
Publishers. The library provides easy ways to store your authentication 
credentials and log SOAP interactions. It also contains example code to help you
get started integrating with our APIs.


##How do I get started?
Install or update the library from PyPI. If you're using pip, this is as easy
as:

`$ pip install [--upgrade] adspygoogle`

If you don't want to install directly from PyPI, you can download the library
as a tarball and then install it manually. The download can be found here:
https://pypi.python.org/pypi/adspygoogle
Navigate to the directory that contains your downloaded unzipped client
library and run the "setup.py" script to install the "adspygoogle"
module.

`$ python setup.py build install`

You can find code examples in the git repo and in the library's releases within
the examples folder.

##Where do I submit bug reports and/or feature requests?

Use the issue tracker at:
  https://github.com/googleads/google-api-ads-python/issues

Make sure to subscribe to our Google Plus page for API change announcements and
other news:

  https://plus.google.com/+GoogleAdsDevelopers


##External Dependencies:


    - Python v2.4+         -- http://www.python.org/
    - PyXML v0.8.3+        -- http://sourceforge.net/projects/pyxml/
                           or
      ElementTree v1.2.6+  -- http://effbot.org/zone/element-index.htm
                           or
      cElementTree v1.0.6+ -- http://www.python.org/
                           (part of the Python v2.5+)
                           or
      lxml v2.2+           -- http://codespeak.net/lxml/index.html
    - fpconst              -- http://pypi.python.org/pypi/fpconst/#downloads
    - oauth2client         -- http://code.google.com/p/google-api-python-client/downloads/list
                           (only if using oauth2)
    - Epydoc               -- http://epydoc.sourceforge.net/
                           (only if you will be generating docs)
    - mock                 -- http://pypi.python.org/pypi/mock
                           (only needed to run unit tests)


##Authors:
    api.sgrinberg@gmail.com (Stan Grinberg)
    api.jdilallo@gmail.com (Joseph DiLallo)

##Maintainers:
    api.jdilallo@gmail.com (Joseph DiLallo)
