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

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_render.sh'
else:
    HANDLER = __root__ + '\srs_render.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')
c4dCommandLineExecutable = config.get(srs_functions.CONFIG_SECTION, 'c4dCommandLineExecutable')
outputToFramesDir = srs_functions.get_config_directory(os.path.join('projects', 'frames'))
outputToPsdsDir = srs_functions.get_config_directory(os.path.join('projects', 'psds'))
srsDomain = config.get(srs_functions.CONFIG_SECTION, 'srsDomain')

# ===================================================================
def handle_render(c4dProjectDir, downloadPWADir, c4dProjectWithAssets, rangeFrom, rangeTo, outputFormat, submittedByUserApiToken):
# ===================================================================
    # Submits a background job to render one or more frames
    # .....................................................

    if True == verbose:
        print("*** Passing render script to handler: ", HANDLER, ", with ", c4dCommandLineExecutable)

    if True == verbose:
        print("Processing c4dProjectWithAssets: ", downloadPWADir, '/', c4dProjectWithAssets, ' from: ', rangeFrom, ' to: ', rangeTo, ' outputFormat: ', outputFormat)

    """
    NB COMMENTED OUT THIS EXPERIMENTAL SECTION

    # Use subprocess to call the shell script
    try:
        print("Running shell script")
        subprocess.run(['bash', HANDLER, c4dCommandLineExecutable, c4dProjectDir, downloadPWADir, c4dProjectWithAssets, str(rangeFrom), str(rangeTo), outputFormat, outputToFramesDir, outputToPsdsDir, srsDomain, email, apiToken, submittedByUserApiToken], check=True)

        # Windows version
        # subprocess.run(['cmd.exe', '/c', shell_script_path, param1, param2], check=True)

        print("Shell script executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell script: {e}")
    except FileNotFoundError:
        print(f"Shell script not found at {HANDLER}")
    except Exception as e:
        print(f"An error occurred: {e}")

    """

    try:
        # We send the current user email address for validation and the submitted by token to
        # find out which render id is being processed
        p = subprocess.Popen([HANDLER, c4dCommandLineExecutable, c4dProjectDir, downloadPWADir, c4dProjectWithAssets, str(rangeFrom), str(rangeTo), outputFormat, outputToFramesDir, outputToPsdsDir, srsDomain, email, apiToken, submittedByUserApiToken])
        p.communicate()

    except Exception as e:
        message = "Error trying to render. Error message: " + str(e)
        print(message)
        gui.MessageDialog(message)

    try:
        gui.MessageDialog("Done rendering")

    except Exception as e:
        message = "Error trying to show gui dialogue. Error message: " + str(e)
        print(message)

    if True == verbose:
        print("Render completed")
