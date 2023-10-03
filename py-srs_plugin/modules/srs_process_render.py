"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge
"""
import os, sys, time
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_render.sh'
else:
    HANDLER = __root__ + '\srs_render.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
input_params = sys.argv

email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')
c4dCommandLineExecutable = config.get(srs_functions.CONFIG_SECTION, 'c4dCommandLineExecutable')
outputToFramesDir = srs_functions.get_plugin_directory(os.path.join('projects', 'frames'))
outputToPsdsDir = srs_functions.get_plugin_directory(os.path.join('projects', 'psds'))
srsDomain = srs_functions.get_srs_domain()

# ===================================================================
def process_render(c4dProjectDir=input_params[1], downloadPWADir=input_params[2], c4dProjectWithAssets=input_params[3], rangeFrom=input_params[4], rangeTo=input_params[5], outputFormat=input_params[6], submittedByUserApiToken=input_params[7]):
# ===================================================================
    # Submits a background job to render one or more frames
    # .....................................................

    if True == verbose:
        print("*** Passing render script to handler: ", HANDLER, ", with ", c4dCommandLineExecutable)

    if True == verbose:
        print("Processing c4dProjectWithAssets: ", downloadPWADir, '/', c4dProjectWithAssets, ' from: ', rangeFrom, ' to: ', rangeTo, ' outputFormat: ', outputFormat)

    try:
        # We send the current user email address for validation and the submitted by token to
        # find out which render id is being processed
        p = subprocess.run([HANDLER, c4dCommandLineExecutable, c4dProjectDir, downloadPWADir, c4dProjectWithAssets, str(rangeFrom), str(rangeTo), outputFormat, outputToFramesDir, outputToPsdsDir, srsDomain, email, apiToken, submittedByUserApiToken], capture_output=True, text=True)
        #print(p)
        #print("Std out: ", p.stdout)
        #print("Std err: ", p.stderr)

    except Exception as e:
        message = "Error trying to render. Error message: " + str(e)
        print(message)
        print(e.args)

    if True == verbose:
        print("Render completed")

# Invoke the process render function
if __name__=="__main__":
    process_render()

    print("COMPLETED: Render subprocess completed")