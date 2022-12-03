"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description: Handle HTTP connections

"""
import json, urllib, urllib2
import srs_functions

ERROR = "Error"
OK = "OK"

config = srs_functions.get_config_values()
debug = bool(config.get(srs_functions.CONFIG_SECTION, 'debug'))
    
def submitRequest(self, endPoint, sendData):
    """ 
        Submit a POST request to the master node

        Returns:
            bool: False on error else True.
    """     
    # Submmit the POST request       
    sendData = urllib.urlencode(sendData)
    
    if True == debug:
        print "Submitting to ", endPoint, ", details: ", sendData
    request = urllib2.Request(endPoint, sendData)
    response = urllib2.urlopen(request)
        
    error = False
    if 200 == response.code:
        if True == debug:
            print "Submitted OK to end point: ", endPoint
    else:
        # Alwayas print the error message
        print "Unexpected response code from end point: ", endPoint, " with response code: ", response.code
        error = True

    responseData = json.loads(response.read())
    response.close()
    
    if True == debug:
        print "Returned data: ", responseData
    
    if ERROR == responseData['result']:
        error = True
        # Alwayas print the error message
        print "Error in request: ", responseData['message']
    
    return error
    
    
    
    