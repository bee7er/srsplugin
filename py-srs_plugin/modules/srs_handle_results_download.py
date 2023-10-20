"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import os, time, subprocess
import srs_functions, srs_connections

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadResults.sh'
else:
    HANDLER = __root__ + '\srs_downloadResults.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')
outputToDir = srs_functions.get_plugin_directory(os.path.join('projects', 'downloads', 'results'))
srsDomain = srs_functions.get_srs_domain()
srsApi = config.get(srs_functions.CONFIG_SECTION, 'srsApi')
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')

# Config settings
EMAIL = "email"
APITOKEN = "apiToken"
FILENAME = "fileName"

# ===================================================================
def handle_results_download(frameDetails):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    try:
        if True == verbose:
            print("*** Downloading frame ranges: ", frameDetails)

        __modules__ = os.path.dirname(__file__)
        process_results_download = os.path.join(__modules__, "srs_process_results_download.py")

        for frameDetail in frameDetails:
            if True == verbose:
                print(frameDetail, "\n")

            print("******* Downloading IMAGE: ", frameDetail, "\n")
            p = subprocess.run(["python3", process_results_download, c4dProjectWithAssets, frameDetail, outputToDir, srsDomain, apiToken], capture_output=True, text=True)
            print("******* Housekeeping IMAGE: ", frameDetail, "\n")
            responseData = srs_connections.submitRequest(
                    (srsApi + "/downloaded"),
                    {EMAIL:email, APITOKEN:apiToken, FILENAME:frameDetail}
                )
            if 'Error' == responseData['result']:
                print("Error in housekeeping: ", responseData['message'])
                return

        if True == debug:
            print("Std out: ", p.stdout)
            print("Std err: ", p.stderr)

        return {'result': "OK", 'message': "Download of results completed"}

    except Exception as e:
        message = "Error trying to download results. Error message: " + str(e)
        print(message)
        print(e.args)

        return {'result': 'Error', 'message': message}
