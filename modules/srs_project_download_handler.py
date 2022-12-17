"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

HANDLER = __root__ + '/srs_downloadProject.sh'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
downloadPWADir = config.get(srs_functions.CONFIG_SECTION, 'downloadPWADir')

# ===================================================================
def handle_project_download(c4dProjectWithAssets):
# ===================================================================
    # Downloading the project with assets file from master
    # .....................................................
    code = 'Init'
    try:
        if True == debug:
            print "*** Downloading project with assets file to: ", downloadPWADir
            print "*** Downloading project with assets dir to: ", c4dProjectWithAssets

        code = subprocess.Popen([HANDLER, c4dProjectWithAssets, downloadPWADir])

        if True == verbose:
            print "Submission of project with assets file with result code: ", code

        return {'result': "OK", 'message': "Download of project with assets file completed"}

    except:
        message = "Error trying to download. Please check your internet connection. Code = " + code
        print message
        return {'result': 'Error', 'message': message}
