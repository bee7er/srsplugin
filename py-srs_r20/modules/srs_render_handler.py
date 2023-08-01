"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Command line rendering:
        NB Since R21 you have to login to the command line every now and again:
        Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>
"""
import c4d, os, time
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_render.sh'
else:
    HANDLER = __root__ + '\srs_render.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')
c4dCommandLineDir = config.get(srs_functions.CONFIG_SECTION, 'c4dCommandLineDir')
outputToFramesDir = config.get(srs_functions.CONFIG_SECTION, 'outputToFramesDir')
outputToPsdsDir = config.get(srs_functions.CONFIG_SECTION, 'outputToPsdsDir')
srsDomain = config.get(srs_functions.CONFIG_SECTION, 'srsDomain')

# ===================================================================
def handle_render(c4dProjectDir, downloadPWADir, c4dProjectWithAssets, rangeFrom, rangeTo, outputFormat, submittedByUserApiToken):
# ===================================================================
    # Submits a background job to render one or more frames
    # .....................................................

    if True == verbose:
        print("*** Submitting render script: ", HANDLER, ", with ", c4dCommandLineDir)

    if True == verbose:
        print("Submitting c4dProjectWithAssets: ", downloadPWADir, '/', c4dProjectWithAssets, ' from: ', rangeFrom, ' to: ', rangeTo, ' outputFormat: ', outputFormat)

    # We send the current user email address for validation and to find out which render id is being processed
    p = subprocess.Popen([HANDLER, c4dCommandLineDir, c4dProjectDir, downloadPWADir, c4dProjectWithAssets, str(rangeFrom), str(rangeTo), outputFormat, outputToFramesDir, outputToPsdsDir, srsDomain, email, apiToken, submittedByUserApiToken])
    p.communicate()

    if True == verbose:
        print("Render completed")
