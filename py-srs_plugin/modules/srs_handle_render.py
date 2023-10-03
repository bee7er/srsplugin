"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Command line rendering:
        NB Since R21 you have to login to the command line to state from where the licence is coming:
        Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

        In the rendering process on the command line, one gets:

            Error running authentication: No License Model defined [license_impl.cpp(146)]
            ----
            Enter the license method:
              1) Maxon App
              2) Maxon Account
              3) Maxon License Server
              4) RLM
              Q) Quit
            Please select: 1
            License okay.

        Following this initialisation of the licence on the command line the render plugin worked
"""
import c4d, os, time
from c4d import gui
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')
outputToFramesDir = srs_functions.get_plugin_directory(os.path.join('projects', 'frames'))
outputToPsdsDir = srs_functions.get_plugin_directory(os.path.join('projects', 'psds'))
srsDomain = srs_functions.get_srs_domain()

# ===================================================================
def handle_render(c4dProjectDir, downloadPWADir, c4dProjectWithAssets, rangeFrom, rangeTo, outputFormat, submittedByUserApiToken):
# ===================================================================
    # Submits a background job to render one or more frames
    # .....................................................
    if True == verbose:
        print("*** Passing render script to handler: ", HANDLER, ", with ", c4dCommandLineExecutable)

    if True == verbose:
        print("Processing c4dProjectWithAssets: ", downloadPWADir, '/', c4dProjectWithAssets, ' from: ', rangeFrom, ' to: ', rangeTo, ' outputFormat: ', outputFormat)

    try:
        __modules__ = os.path.dirname(__file__)
        process_render = os.path.join(__modules__, "srs_process_render.py")

        p = subprocess.run(["python3", process_render, c4dProjectDir, downloadPWADir, c4dProjectWithAssets, str(rangeFrom), str(rangeTo), outputFormat, submittedByUserApiToken], capture_output=True, text=True)
        #print(p)
        #print("Std out: ", p.stdout)
        #print("Std err: ", p.stderr)

    except Exception as e:
        message = "Error trying to render. Error message: " + str(e)
        print(message)
        print(e.args)

    if True == verbose:
        print("Render submitted")
