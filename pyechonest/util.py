#!/usr/bin/env python
# encoding: utf-8
"""
Utility functions to support the Echo Nest web API interface.  This
module is not meant for other uses and should not be used unless
modifying or extending the package.
"""

import urllib
import urllib2
import config
import logging
import simplejson as json
import socket

SUCCESS_STATUS_CODES = ( 0, )
FAILURE_THING_ID_STATUS_CODES = (7, 6)
FAILURE_API_KEY_STATUS_CODES = (12,)

class EchoNestAPIError(Exception):
    """
    Generic API errors. 
    """
    def __init__(self, code, message):
        self.code = code
        self._message = message
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return 'Echo Nest API Error %d: %s' % (self.code, self._message)

def verify_successful(response_dict):
    status_dict = response_dict['response']['status']
    code = int(status_dict['code'])
    message = status_dict['message']
    if (code != 0):
        # do some cute exception handling
        raise EchoNestAPIError(code, message)
    del response_dict['response']['status']


def callm(method, param_dict, POST=False, socket_timeout=10):
    '''
    Call the api! 
    Param_dict is a *regular* *python* *dictionary* so if you want to have multi-valued params
    put them in a list.
    '''
    param_dict['api_key'] = config.ECHO_NEST_API_KEY
    param_list = []
    
    for key,val in param_dict.iteritems():
        if isinstance(val, list):
            param_list.extend( [(key,subval) for subval in val] )
        else:
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            param_list.append( (key,val) )
    logging.debug("PARAMS: %s" % str(param_list))
    params = urllib.urlencode(param_list)
    socket.setdefaulttimeout(socket_timeout)
    if(POST):
        url = 'http://%s/%s/%s/%s' % (config.API_HOST, config.API_SELECTOR, config.API_VERSION, method)
        f = urllib.urlopen(url, params)
    else:
        url = 'http://%s/%s/%s/%s?%s' % (config.API_HOST, config.API_SELECTOR, config.API_VERSION, 
                                    method, params)
        f = urllib.urlopen(url)
    socket.setdefaulttimeout(None)
    if config.TRACE_API_CALLS:
        logging.info(url)
    response_dict = json.loads(f.read())
    verify_successful(response_dict)
    return response_dict


def postChunked(host, selector, fields, files):
    """
    Attempt to replace postMultipart() with nearly-identical interface.
    (The files tuple no longer requires the filename, and we only return
    the response body.) 
    Uses the urllib2_file.py originally from 
    http://fabien.seisen.org which was also drawn heavily from 
    http://code.activestate.com/recipes/146306/ .

    This urllib2_file.py is more desirable because of the chunked 
    uploading from a file pointer (no need to read entire file into 
    memory) and the ability to work from behind a proxy (due to its 
    basis on urllib2).
    """
    params = urllib.urlencode(fields)
    url = 'http://%s%s?%s' % (host, selector, params)
    u = urllib2.urlopen(url, files)
    result = u.read()
    [fp.close() for (key, fp) in files]
    return result

class attrdict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


