"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadProject.sh'
else:
    HANDLER = __root__ + '\srs_downloadProject.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
downloadPWADir = config.get(srs_functions.CONFIG_SECTION, 'downloadPWADir')
srsDomain = config.get(srs_functions.CONFIG_SECTION, 'srsDomain')

# ===================================================================
def handle_project_download(c4dProjectWithAssets):
# ===================================================================
    # Downloading the project with assets file from master
    # .....................................................
    code = 'Init'
    try:
        if True == verbose:
            print "*** Downloading handler: ", HANDLER
            print "*** Downloading project with assets file to: ", downloadPWADir
            print "*** Downloading project with assets dir to: ", c4dProjectWithAssets

        code = subprocess.Popen([HANDLER, c4dProjectWithAssets, downloadPWADir, srsDomain])

        if True == verbose:
            print "Submission of project with assets file with result code: ", code

        return {'result': "OK", 'message': "Download of project with assets file completed"}

    except:
        message = "Error trying to download. Please check your internet connection. Code = " + code
        print message
        return {'result': 'Error', 'message': message}
