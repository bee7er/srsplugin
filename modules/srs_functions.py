"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge
"""
import c4d, os
import ConfigParser
from ConfigParser import SafeConfigParser

__root__ = os.path.dirname(os.path.dirname(__file__))

CONFIG_FILE = __root__ + '/config/properties.ini'
CONFIG_SECTION = 'CONFIG'
CONFIG_REGISTRATION_SECTION = 'REGISTRATION'
CONFIG_RENDER_SECTION = 'RENDER'

RANGE_FROM = "RANGE_FROM"
RANGE_TO = "RANGE_TO"
RANGE_STEP = "RANGE_STEP"
FRAME_RATE = "FRAME_RATE"
OUTPUT_FORMAT = "OUTPUT_FORMAT"

# ===================================================================
def get_config_values():
# ===================================================================
    # Returns entries in the config file
    # .....................................................

    config = SafeConfigParser()
    # Replace the translate function with 'str', which will stop ini field names from being lower cased
    config.optionxform = str
    config.read(CONFIG_FILE)
      
    return config;   

# ===================================================================
def update_config_values(section, configFields):
# ===================================================================
    # Updates a list of tuples of config field name and values
    # .....................................................

    config = get_config_values()
    verbose = config.get(CONFIG_SECTION, 'verbose')
    
    # configfields is a list of tuples:
    #    [('field name', 'field value'), ('field name', 'field value'), ...]
    #
    for field in configFields:
        if True == verbose:
            print "Config out: ", field[0], field[1]
        config.set(section, field[0], field[1])
        
    with open(CONFIG_FILE, 'w') as configFile:
        config.write(configFile)
        
    return config 

# ===================================================================
def analyse_frame_ranges(frameRangeStr):
# ===================================================================
    # Analyses a string of frame ranges, validates them and returns a list of them
    # .....................................................

    config = get_config_values()
    verbose = config.get(CONFIG_SECTION, 'verbose')
    
    # Remove all spaces
    frameRangeLst = frameRangeStr.replace(' ', '').split(',')
    returnStr = ''
    for entry in frameRangeLst:
        # Range should be number-number
        rangelet = entry.split('-')
        if True == verbose:
            print "Ranglet: ", rangeLet
        if 2 != len(rangeLet):
            if True == verbose:
                print "Error: Ignoring invalid rangelet: ", str(rangeLet)
            continue
        elif True != str(rangeLet[0]).isdigit() or True != str(rangeLet[1]).isdigit():
            if True == verbose:
                print "Error: Ignoring non-integer rangelet: ", str(rangeLet)
            continue
        elif int(rangeLet[1]) < int(rangeLet[0]):
            el = rangeLet[0]
            rangeLet[0] = rangeLet[1]
            rangeLet[1] = el
            
        returnStr += str(rangeLet)
        
    return returnStr

# ===================================================================
def get_render_settings():
# ===================================================================
    # Gets render settings from the current active set
    # .....................................................

    activeDocument = c4d.documents.GetActiveDocument()
    renderData = activeDocument.GetActiveRenderData()
    
    return {
        RANGE_FROM: int(renderData[c4d.RDATA_FRAMEFROM].Get() * renderData[c4d.RDATA_FRAMERATE]),
        RANGE_TO: int(renderData[c4d.RDATA_FRAMETO].Get() * renderData[c4d.RDATA_FRAMERATE]),
        RANGE_STEP: renderData[c4d.RDATA_FRAMESTEP],
        FRAME_RATE: int(renderData[c4d.RDATA_FRAMERATE]),
        OUTPUT_FORMAT: int(renderData[c4d.RDATA_FORMAT]),
    }

# ===================================================================
def get_projectWithAssets():
# ===================================================================
    # Gets projectWithAssets path and name from the currently loaded project
    # .....................................................

    config = get_config_values()
    debug = config.get(CONFIG_SECTION, 'debug')
    verbose = config.get(CONFIG_SECTION, 'verbose')

    md = c4d.documents.GetActiveDocument()
    fp = c4d.documents.BaseDocument.GetDocumentPath(md)
    c4dProjectWithAssets = ''
    if '' == fp:
        if True == debug:
            print("*** A project has not been opened")
    else:
        c4dProjectWithAssets = fp + '/' + c4d.documents.BaseDocument.GetDocumentName(md)
        if True == verbose:
            print("Project opened is: ", c4dProjectWithAssets)

    return c4dProjectWithAssets
