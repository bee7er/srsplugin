"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description: Handle HTTP connections

"""

VERSION = "R2023"
try:
    import urllib.parse as parser
    import urllib.request as requester
    print("Connecting with R2023")
except:
    import urllib, urllib2
    print("Connecting with R20")
    VERSION = "R20"

import srs_functions
import c4d
from c4d import gui
import json

ERROR = "Error"
OK = "OK"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# ===================================================================
def submitRequest(
    self,
    endPoint,
    sendData
    ):
# ===================================================================
    # Submit a POST request to the master node
    # .....................................................

    if "R2023" == VERSION:
        sendData = parser.urlencode(sendData)
    else:
        sendData = urllib.urlencode(sendData)

    if True == verbose:
        print("*** Submitting to ", endPoint, ", details: ", sendData)

    responseData = 'None'
    try:
        if "R2023" == VERSION:
            response = requester.urlopen(endPoint, bytes(sendData, 'utf-8'))
        else:
            request = urllib2.Request(endPoint, sendData)
            response = urllib2.urlopen(request)

        error = False
        if 200 == response.code:
            if True == verbose:
                print("Submitted OK to end point: ", endPoint)
        else:
            # Always print the error message
            error = "Unexpected response code from end point: ", endPoint, " with response code: ", response.code
            print(error)
            return {'result': 'Error', 'message': error}

        responseData = json.loads(response.read())

        response.close()

    except Exception as e:
        message = "Error trying to connect. Please check your internet connection. Error message: " + str(e)
        print(message)
        gui.MessageDialog(message)
        return {'result': 'Error', 'message': message}

    if True == verbose:
        print("*** Returned data: ", responseData)

    return responseData
