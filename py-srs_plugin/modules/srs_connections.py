"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description: Handle HTTP connections

"""

VERSION = "R2023+"
try:
    import urllib.parse as parser
    import urllib.request as requester
except:
    import urllib, urllib2
    print("Connecting with R20 syntax")
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
    endPoint,
    sendData
    ):
# ===================================================================
    # Submit a POST request to the master node
    # .....................................................

    if "R2023+" == VERSION:
        sendData = parser.urlencode(sendData)
    else:
        sendData = urllib.urlencode(sendData)

    if True == verbose:
        print("*** Submitting to ", endPoint, ", details: ", sendData)

    responseData = 'None'
    try:
        print("*** 1 ")

        if "R2023+" == VERSION:
            print("*** 1.1 ")
            response = requester.urlopen(endPoint, bytes(sendData, 'utf-8'))
            print("*** 1.2 ")
        else:
            request = urllib2.Request(endPoint, sendData)
            response = urllib2.urlopen(request)

        print("*** 2 ")

        error = False
        if 200 == response.code:
            if True == verbose:
                print("Submitted OK to end point: ", endPoint)
        else:
            # Always print the error message
            error = "Unexpected response code from end point: ", endPoint, " with response code: ", response.code
            print(error)
            return {'result': 'Error', 'message': error}

        print("*** 3 ")

        responseData = json.loads(response.read())

        print("*** 4 ")

        response.close()

        print("*** 5 ")

    except Exception as e:
        message = "Error trying to connect. Please check your internet connection. Error message: " + str(e)
        print(message)
        gui.MessageDialog(message)
        return {'result': 'Error', 'message': message}

    if True == verbose:
        print("*** Returned data: ", responseData)

    print("*** 6 ")

    return responseData
