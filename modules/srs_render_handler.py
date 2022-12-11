"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Command line rendering:

        NB Since R21 you have to login to the command line every now and again:
        Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

        /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/srs_functions.c4d -frame 0 5 -oimage ~/Code/c4d/srs/frames/srs -omultipass ~/Code/c4d/test_mp -oformat TIFF
        /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/RedshiftTest.c4d -frame 0 5 -oimage ~/Code/c4d/srs/frames/srs -omultipass ~/Code/c4d/test_mp -oformat PNG
        /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/RedshiftTest.c4d -oimage ~/Code/c4d/srs/redshifttest/frames/redshifttest -omultipass ~/Code/c4d/test_mp

"""
import c4d, os, time
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

HANDLER = __root__ + '/render.sh'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
# Params
c4dCommandLine = config.get(srs_functions.CONFIG_SECTION, 'c4dCommandLine')
c4dProjectWithAssets = 'internal data'
frameRange = 'submitted data'
outputType = 'submitted data'
outputFrames = 'ini'
outputPsds = 'ini'

# ===================================================================
def handle_render():
# ===================================================================
    # Submits a background job to render one or more frames
    # .....................................................

    if True == debug:
        print "*** Submitting render script: ", HANDLER, ", with ", c4dCommandLine

    code = subprocess.Popen([HANDLER, c4dCommandLine])

    if True == verbose:
        print "Submission result code: ", code
