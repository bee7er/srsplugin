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

# ===================================================================
def handle_results_download(frameRanges):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    code = 'Init'
    try:
        if True == debug:
            print "*** Downloading frame ranges: ", frameRanges



# TODO Iterate the frame ranges, build the name and call the download handler



        code = subprocess.Popen([HANDLER, frameRanges])

        if True == verbose:
            print "Submission of results file with result code: ", code

        return {'result': "OK", 'message': "Download of results with assets file completed"}

    except:
        message = "Error trying to download results. Please check your internet connection. Code = " + code
        print message
        return {'result': 'Error', 'message': message}
