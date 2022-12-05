"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

HANDLER = __root__ + '/render.sh'

config = srs_functions.get_config_values()
debug = bool(config.get(srs_functions.CONFIG_SECTION, 'debug'))

# Submits a job to render one or more frames
def handle_render():
    """
        Submit a render process to a background job
    """
    if True == debug:
        print "Submitting render script: " + HANDLER

    code = subprocess.Popen(HANDLER)

    if True == debug:
        print "Submission result code: ", code
