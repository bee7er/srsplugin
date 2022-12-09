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
debug = bool(config.get(srs_functions.CONFIG_SECTION, 'debug'))
c4dCommandLine = config.get(srs_functions.CONFIG_SECTION, 'c4dCommandLine')

# Submits a background job to render one or more frames
def handle_render():
    """
        Submit a render process to a background job on this slave
    """

    if True == debug:
        print "Submitting render script: ", HANDLER, ", with ", c4dCommandLine

    code = subprocess.Popen([HANDLER, c4dCommandLine])

    if True == debug:
        print "Submission result code: ", code
