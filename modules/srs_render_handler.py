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

HANDLER = __root__ + '/srs_render.sh'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
c4dCommandLineDir = config.get(srs_functions.CONFIG_SECTION, 'c4dCommandLineDir')
outputToFramesDir = config.get(srs_functions.CONFIG_SECTION, 'outputToFramesDir')
outputToPsdsDir = config.get(srs_functions.CONFIG_SECTION, 'outputToPsdsDir')
srsApi = config.get(srs_functions.CONFIG_SECTION, 'srsApi')

# ===================================================================
def handle_render(c4dProjectDir, downloadPWADir, c4dProjectWithAssets, rangeFrom, rangeTo, outputFormat):
# ===================================================================
    # Submits a background job to render one or more frames
    # .....................................................

    if True == verbose:
        print "*** Submitting render script: ", HANDLER, ", with ", c4dCommandLineDir

    if True == verbose:
        print "Submitting c4dProjectWithAssets: ", downloadPWADir, '/', c4dProjectWithAssets, ' from: ', rangeFrom, ' to: ', rangeTo, ' outputFormat: ', outputFormat

    code = subprocess.Popen([HANDLER, c4dCommandLineDir, c4dProjectDir, downloadPWADir, c4dProjectWithAssets, str(rangeFrom), str(rangeTo), outputFormat, outputToFramesDir, outputToPsdsDir, srsApi])

    if True == verbose:
        print "Submission result code: ", code
