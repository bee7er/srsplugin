"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description: Handle HTTP connections

"""
import json, urllib, urllib2
import srs_functions
import c4d
from c4d import gui
ERROR = "Error"
OK = "OK"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# ===================================================================
def submitRequest(self, endPoint, sendData):
# ===================================================================
    # Submit a POST request to the master node
    # .....................................................

    sendData = urllib.urlencode(sendData)
    
    if True == verbose:
        print "*** Submitting to ", endPoint, ", details: ", sendData

    try:
        request = urllib2.Request(endPoint, sendData)
        response = urllib2.urlopen(request)

        error = False
        if 200 == response.code:
            if True == verbose:
                print "Submitted OK to end point: ", endPoint
        else:
            # Always print the error message
            error = "Unexpected response code from end point: ", endPoint, " with response code: ", response.code
            print error
            return {'result': 'Error', 'message': error}

        responseData = json.loads(response.read())
        response.close()
    except:
        message = "Error trying to connect. Please check your internet connection."
        print message
        gui.MessageDialog(message)
        return {'result': 'Error', 'message': message}
    
    if True == verbose:
        print "*** Returned data: ", responseData
    
    return responseData
    
    
    
    