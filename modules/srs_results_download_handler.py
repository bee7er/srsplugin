"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadResults.sh'
else:
    HANDLER = __root__ + '\srs_downloadResults.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')
downloadPWADir = config.get(srs_functions.CONFIG_SECTION, 'downloadPWADir')
outputToFramesDir = config.get(srs_functions.CONFIG_SECTION, 'outputToFramesDir')
outputToPsdsDir = config.get(srs_functions.CONFIG_SECTION, 'outputToPsdsDir')
srsDomain = config.get(srs_functions.CONFIG_SECTION, 'srsDomain')

# ===================================================================
def handle_results_download(frameRanges):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    code = 'Init'
    try:
        if True == verbose:
            print "*** Downloading frame ranges: ", frameRanges


        for frameRange in frameRanges:
            print frameRange, "\n"

            code = subprocess.Popen([HANDLER, c4dProjectWithAssets, frameRange, downloadPWADir, outputToFramesDir, outputToPsdsDir, srsDomain])

        if True == verbose:
            print "Download of results file with result code: ", code

        return {'result': "OK", 'message': "Download of results with assets file completed"}

    except:
        message = "Error trying to download results. Please check your internet connection. Code = " + code
        print message
        return {'result': 'Error', 'message': message}
