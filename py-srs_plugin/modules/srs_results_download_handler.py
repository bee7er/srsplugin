"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadResults.sh'
else:
    HANDLER = __root__ + '\srs_downloadResults.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')
downloadPWADir = srs_functions.get_plugin_directory(os.path.join('projects', 'downloads'))
outputToFramesDir = srs_functions.get_plugin_directory(os.path.join('projects', 'frames'))
outputToPsdsDir = srs_functions.get_plugin_directory(os.path.join('projects', 'psds'))
srsDomain = config.get(srs_functions.CONFIG_SECTION, 'srsDomain')
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')

# ===================================================================
def handle_results_download(frameDetails):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    code = 'Init'
    try:
        if True == verbose:
            print("*** Downloading frame ranges: ", frameDetails)


        for frameDetail in frameDetails:
            if True == verbose:
                print(frameDetail, "\n")

            print("Downloading: ", frameDetail, "\n")

            p = subprocess.Popen([HANDLER, c4dProjectWithAssets, frameDetail, downloadPWADir, outputToFramesDir, outputToPsdsDir, srsDomain, apiToken])
            p.communicate()

        if True == verbose:
            print("Download of results file completed")

        return {'result': "OK", 'message': "Download of results completed"}

    except:
        message = "Error trying to download results. Please check your internet connection."
        print(message)
        return {'result': 'Error', 'message': message}
