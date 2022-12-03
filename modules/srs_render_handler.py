"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description:

"""
import c4d, os
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

HANDLER = __root__ + '/render.sh'

# Submits a job to render one or more frames
def handle_render():
    config = srs_functions.get_config_values()
    debug = config.get(srs_functions.CONFIG_SECTION, 'debug')
    
    if True == debug:
        print "Submitting render script: " + HANDLER
    
    code = subprocess.call([HANDLER, 'param'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    if True == debug:
        print "Submission result code: ", code
