"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

HANDLER = __root__ + '/srs_downloadResults.sh'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')
downloadPWADir = config.get(srs_functions.CONFIG_SECTION, 'downloadPWADir')

# ===================================================================
def handle_results_download(frameRanges):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    code = 'Init'
    try:
        if True == debug:
            print "*** Downloading frame ranges: ", frameRanges


        for frameRange in frameRanges:
            print frameRange, "\n"

            code = subprocess.Popen([HANDLER, c4dProjectWithAssets, frameRange, downloadPWADir])

        if True == verbose:
            print "Download of results file with result code: ", code

        return {'result': "OK", 'message': "Download of results with assets file completed"}

    except:
        message = "Error trying to download results. Please check your internet connection. Code = " + code
        print message
        return {'result': 'Error', 'message': message}
