"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge
"""
import os, platform

try:
    # R2023
    import configparser as configurator
    print("Running 2023")
except:
    # Prior to R2023
    import ConfigParser as configurator
    print("Running prior version to 2023")

__root__ = os.path.dirname(os.path.dirname(__file__))

RANGE_FROM = "RANGE_FROM"
RANGE_TO = "RANGE_TO"
RANGE_STEP = "RANGE_STEP"
FRAME_RATE = "FRAME_RATE"
OUTPUT_FORMAT = "OUTPUT_FORMAT"

OS_MAC = 'mac'
OS_UNKNOWN = 'unknown'
OS_WINDOWS = 'windows'

# ===================================================================
def get_config_values():
# ===================================================================
    # Returns entries in the config file
    # .....................................................

    config = configurator.ConfigParser()
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
        apiDtls = srsApi.split('/')
        return (apiDtls[0] + '//' + apiDtls[2])

    except Exception as e:
        print("Error parsing API URL: " + str(e))

# ===================================================================
def validate_config_values(config):
# ===================================================================
    """
        Validate the config values
    """
    validationResult = []

    # Validate the CONFIG section
    if "" == config.get(CONFIG_SECTION, 'srsApi').strip():
        validationResult.append("Property 'srsApi' has not been set")

    if "" == config.get(CONFIG_SECTION, 'c4dCommandLineExecutable').strip():
        validationResult.append("Property 'c4dCommandLineExecutable' has not been set")
    else:
        if True != os.path.exists(config.get(CONFIG_SECTION, 'c4dCommandLineExecutable').strip()):
            validationResult.append("Commandline Python executable file 'c4dCommandLineExecutable' not found.")

    pwaError = False
    projectWithAssetsDir = config.get(CONFIG_SECTION, 'c4dProjectWithAssetsDir').strip()
    if "" == projectWithAssetsDir:
        pwaError = True
        validationResult.append("Property 'c4dProjectWithAssetsDir' has not been set")
    else:
        # Redefine full path to PWA directory
        projectWithAssetsDir = get_plugin_directory(os.path.join('projects', 'with_assets', projectWithAssetsDir))
        if True != os.path.exists(projectWithAssetsDir):
            pwaError = True
            validationResult.append("Property 'c4dProjectWithAssetsDir', directory not found.")

    projectWithAssets = config.get(CONFIG_SECTION, 'c4dProjectWithAssets').strip()
    if "" == projectWithAssets:
        pwaError = True
        validationResult.append("Property 'c4dProjectWithAssets' has not been set")

    # If no error so far then check the project with assets file exists
    if False == pwaError:
        if True != os.path.exists(os.path.join(projectWithAssetsDir, projectWithAssets)):
            validationResult.append(
                "Properties 'c4dProjectWithAssetsDir' and 'c4dProjectWithAssets' do not locate the project with assets file.  File not found."
                )

    # Validate the REGISTRATION section
    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'email').strip():
        validationResult.append("Property 'email' has not been set")

    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'apiToken').strip():
        validationResult.append("Property 'apiToken' has not been set")

    if "" == config.get(CONFIG_REGISTRATION_SECTION, 'availability').strip():
        validationResult.append("Property 'availability' has not been set")

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

    verbose = True

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

    print('returnStr=', returnStr)
    return returnStr

# Now use the config symbolic constants and access the appropriate .ini file

CONFIG_SECTION = 'CONFIG'
CONFIG_REGISTRATION_SECTION = 'REGISTRATION'
CONFIG_RENDER_SECTION = 'RENDER'

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
        # Unsupported platform
        osName = OS_UNKNOWN

    return osName

CONFIG_FILE = __root__ + '/config/properties.ini'
if OS_MAC == get_platform():
    CONFIG_FILE = __root__ + '/config/properties.ini'
else:
    CONFIG_FILE = __root__ + '/config/properties.ini.win'
