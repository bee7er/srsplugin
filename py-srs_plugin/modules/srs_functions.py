"""
Copyright: Etheridge 2024
Author: Brian Etheridge

PLEASE NOTE:  These utility functions do not need c4d.
Put any that do need c4d into srs_functions_c4d.py

"""
import os, platform, configparser

__root__ = os.path.dirname(os.path.dirname(__file__))

RANGE_FROM = "RANGE_FROM"
RANGE_TO = "RANGE_TO"
RANGE_STEP = "RANGE_STEP"
FRAME_RATE = "FRAME_RATE"
OUTPUT_FORMAT = "OUTPUT_FORMAT"

OS_MAC = 'mac'
OS_UNKNOWN = 'unknown'
OS_WINDOWS = 'windows'

CONFIG_SECTION = 'CONFIG'
CONFIG_REGISTRATION_SECTION = 'REGISTRATION'
CONFIG_RENDER_SECTION = 'RENDER'
PREVIOUSTEAMSMAX = 'previousTeamsMax'
PREVIOUSTEAMTOKENS = 'previousTeamTokens'
C4D_PROJECT_WITH_ASSETS = 'c4dProjectWithAssets'
C4D_PROJECT_WITH_ASSETS_DIR = 'c4dProjectWithAssetsDir'

CONFIG_FILE = os.path.join(__root__, 'config', 'properties.ini')

# ===================================================================
def get_config_values():
# ===================================================================
    # Returns entries in the config file
    # .....................................................

    config = configparser.ConfigParser()
    # Replace the translate function with 'str', which will stop ini field names from being lower cased
    config.optionxform = str
    config.read(CONFIG_FILE)
      
    return config

# ===================================================================
def get_plugin_directory(dir):
# ===================================================================
    # Returns the full path to a plugin directory
    pluginDir, _ = os.path.split(os.path.dirname(__file__))
    return os.path.join(pluginDir, dir)

# ===================================================================
def get_srs_domain():
# ===================================================================
    try:
        config = get_config_values()
        # Get the API URL and derive the domain from that
        srsApi = config.get(CONFIG_SECTION, 'srsApi')
        # Web addresses all use forward slash, not OS dependent
        # Here we effectively remove any trailing slashes and API version details
        apiDtls = srsApi.split('/')
        domain = (apiDtls[0] + '//' + apiDtls[2])

        return domain

    except Exception as e:
        print("Error parsing API URL: " + str(e))

# ===================================================================
def validate_directories(config):
# ===================================================================
    """
        Validate the project directories and create them if not present
    """

    # Check the required directories are present.  If not create them.
    projectsDir = get_plugin_directory(os.path.join('projects'))
    if True != os.path.exists(projectsDir):
        os.mkdir(projectsDir)
    downloadsDir = get_plugin_directory(os.path.join('projects', 'downloads'))
    if True != os.path.exists(downloadsDir):
        os.mkdir(downloadsDir)
    framesDir = get_plugin_directory(os.path.join('projects', 'frames'))
    if True != os.path.exists(framesDir):
        os.mkdir(framesDir)
    with_assetsDir = get_plugin_directory(os.path.join('projects', 'with_assets'))
    if True != os.path.exists(with_assetsDir):
        os.mkdir(with_assetsDir)

    return

# ===================================================================
def validate_config(config):
# ===================================================================
    """
        Validate the config values and operating environment
    """
    validationResult = []

    # Validate the CONFIG section
    if "" == config.get(CONFIG_SECTION, 'srsApi').strip():
        validationResult.append("Property 'srsApi' has not been set")

    # Validate the REGISTRATION section
    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'email').strip():
        validationResult.append("Property 'email' has not been set")

    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'userToken').strip():
        validationResult.append("Property 'userToken' has not been set")

    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'availability').strip():
        validationResult.append("Property 'availability' has not been set")

    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'teamToken').strip():
        message = "\nProperty 'teamToken' has not been set\n"
        message += "Obtain the team token from your team organiser\n"
        message += "Or click New Team to start a new team\n"
        validationResult.append(message)

    if 0 == len(validationResult):
        return True

    return validationResult

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
            print("Config out: ", field[0], field[1])
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
    sep = ''
    for entry in frameRangeLst:
        # Range should be number-number
        rangelet = entry.split('-')
        if True == verbose:
            print("Rangelet: ", rangelet)
        if 1 == len(rangelet):
            # Build a rangelet from what we've been given, e.g. 12 -> 12-12
            rangelet = [rangelet[0], rangelet[0]]
        # Check what we've got
        if 2 < len(rangelet):
            if True == verbose:
                print("Error: Ignoring invalid rangelet: ", str(rangelet))
            continue
        elif True != str(rangelet[0]).isdigit() or True != str(rangelet[1]).isdigit():
            if True == verbose:
                print("Error: Ignoring non-integer rangelet: ", str(rangelet))
            continue
        elif int(rangelet[1]) < int(rangelet[0]):
            el = rangelet[0]
            rangelet[0] = rangelet[1]
            rangelet[1] = el
            
        returnStr += sep + str(rangelet[0]) + '-' + str(rangelet[1])
        sep = ','

    return returnStr

# ===================================================================
def buildPreviousTeamsList(currentTeamToken):
# ===================================================================
    # Add the team to the list, but drop off the earliest team after
    # a configured limit.
    # .....................................................

    config = get_config_values()
    previousTeamsMax = int(config.get(CONFIG_SECTION, PREVIOUSTEAMSMAX))
    previousTeamTokens = config.get(CONFIG_REGISTRATION_SECTION, PREVIOUSTEAMTOKENS).strip()

    # We are going to add to the end of the list
    tokenLst = []
    if '' != previousTeamTokens:
        tokenLst = previousTeamTokens.split(',')

    tokenLst.append(currentTeamToken)
    lstLen = len(tokenLst)
    # We do not keep more than the count, it is a configurable maximum
    while (lstLen > previousTeamsMax):
        # Remove the oldest element
        tokenLst.pop(0)
        lstLen -= 1

    # Only join up the list entries if there is more than one
    newLstStr = ''
    if len(tokenLst) > 1:
        sep = ","
        newLstStr = sep.join(tokenLst)
    else:
        newLstStr = tokenLst[0]

    return newLstStr


# ===================================================================
def get_platform():
# ===================================================================
    # Works out the current platform and returns it
    # .....................................................

    # Which OS is running?
    os_platform = platform.system().lower()
    osName = OS_UNKNOWN
    if "linux" in os_platform:
        # Treat linux as if it is a MAC
        osName = OS_MAC
    elif "darwin" in os_platform:
        osName = OS_MAC
    elif "win" in os_platform:
        osName = OS_WINDOWS
    else:
        print("Error: unsupported platform: ", os_platform, ", may give unexpected behaviour.")
        osName = OS_UNKNOWN

    return osName
