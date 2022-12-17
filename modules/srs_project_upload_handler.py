"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

HANDLER = __root__ + '/uploadProject.sh'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')
c4dProjectWithAssetsDir = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssetsDir')

# ===================================================================
def handle_project_upload():
# ===================================================================
    # Posting the project with assets file to master
    # .....................................................

    # TODO A unique name is needed for the project with assets name
    if True == debug:
        print "*** Submitting project with assets upload script: ", HANDLER, ", with ", c4dProjectWithAssets, ", in ", c4dProjectWithAssetsDir

    code = subprocess.Popen([HANDLER, c4dProjectWithAssets, c4dProjectWithAssetsDir])

    if True == verbose:
        print "Submission of project with assets file with result code: ", code
