"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description:

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

# Returns entries in the config file
def get_config_values():
    config = SafeConfigParser()
    # Replace the translate function with 'str', which will stop ini field names from being lower cased
    config.optionxform = str
    config.read(CONFIG_FILE)
      
    return config;   

# Updates a list of tuples of config field name and values          
def update_config_values(section, configFields):
    config = get_config_values()
    debug = config.get(CONFIG_SECTION, 'debug')
    
    # configfields is a list of tuples:
    #    [('field name', 'field value'), ('field name', 'field value'), ...]
    #
    for field in configFields:
        if True == debug: 
            print "Config out: ", field[0], field[1]
        config.set(section, field[0], field[1])
        
    with open(CONFIG_FILE, 'w') as configFile:
        config.write(configFile)
        
    return config 

# Analyses a string of frame ranges, validates them and returns a list of them
def analyse_frame_ranges(frameRangeStr):
    config = get_config_values()
    debug = config.get(CONFIG_SECTION, 'debug')
    
    # Remove all spaces
    frameRangeLst = frameRangeStr.replace(' ', '').split(',')
    returnStr = ''
    for entry in frameRangeLst:
        # Range should be number-number
        rangelet = entry.split('-')
        if True == debug: 
            print "Ranglet: ", rangeLet
        if 2 != len(rangeLet):
            if True == debug: 
                print "Error: Ignoring invalid rangelet: ", str(rangeLet)
            continue
        elif True != str(rangeLet[0]).isdigit() or True != str(rangeLet[1]).isdigit():
            if True == debug: 
                print "Error: Ignoring non-integer rangelet: ", str(rangeLet)
            continue
        elif int(rangeLet[1]) < int(rangeLet[0]):
            el = rangeLet[0]
            rangeLet[0] = rangeLet[1]
            rangeLet[1] = el
            
        returnStr += str(rangeLet)
        
    return returnStr
    
# Gets render settings from the current active set         
def get_render_settings():
    activeDocument = c4d.documents.GetActiveDocument()
    renderData = activeDocument.GetActiveRenderData()
    
    return {
        RANGE_FROM: int(renderData[c4d.RDATA_FRAMEFROM].Get() * renderData[c4d.RDATA_FRAMERATE]),
        RANGE_TO: int(renderData[c4d.RDATA_FRAMETO].Get() * renderData[c4d.RDATA_FRAMERATE]),
        RANGE_STEP: renderData[c4d.RDATA_FRAMESTEP],
        FRAME_RATE: int(renderData[c4d.RDATA_FRAMERATE])
    }
