"""
Global configuration variables for accessing the Echo Nest web API.
"""

__version__ = "$Revision: 0 $"
# $Source$

import os

if('ECHO_NEST_API_KEY' in os.environ):
    ECHO_NEST_API_KEY = os.environ['ECHO_NEST_API_KEY']
else:
    ECHO_NEST_API_KEY = None


API_HOST = 'beta.developer.echonest.com'

API_SELECTOR = 'api'
"Locations for the Analyze API calls."

API_VERSION = 'v4'
"Version of api to use... only 4 for now"

HTTP_USER_AGENT = 'BETA_PyENAPI'
"""
You may change this to be a user agent string of your
own choosing.
"""

MP3_BITRATE = 128
"""
Default bitrate for MP3 output. Conventionally an
integer divisible by 32kbits/sec.
"""

CACHE = True
"""
You may change this to False to prevent local caching
of API results.
"""

TRACE_API_CALLS = True
"""
If true, API calls will be traced to the console
"""

ANALYSIS_VERSION = 3
"""
Analysis version
"""
