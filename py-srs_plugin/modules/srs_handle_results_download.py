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
teamToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'teamToken')
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
userToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'userToken')

# Config settings
EMAIL = "email"
USERTOKEN = "userToken"
FILENAME = "fileName"
RENDERID = "renderId"
TEAMTOKEN = "teamToken"

# ===================================================================
def handle_results_download(frameDetails):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    try:
        if True == verbose:
            print("Downloading frame ranges: ", frameDetails)

        __modules__ = os.path.dirname(__file__)
        process_results_download = os.path.join(__modules__, "srs_process_results_download.py")

        for renderId in frameDetails:

            for frameDetail in frameDetails[renderId]:

                if True == verbose:
                    print(frameDetail, "\n")

                p = subprocess.run(["python3", process_results_download,
                    c4dProjectWithAssets,
                    frameDetail,
                    outputToDir,
                    srsDomain,
                    userToken,
                    str(renderId)], capture_output=True, text=True)

                print("Housekeeping 'downloaded' IMAGE on server: ", frameDetail, "\n")
                responseData = srs_connections.submitRequest(
                        (srsApi + "/downloaded"),
                        {TEAMTOKEN: teamToken, EMAIL:email, USERTOKEN:userToken, RENDERID:renderId, FILENAME:frameDetail}
                    )
                if 'Error' == responseData['result']:
                    print("Error in housekeeping: ", responseData['message'])
                    return

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        return {'result': "OK", 'message': "Download of results completed"}

    except Exception as e:
        message = "Error trying to handle download results. Error message: " + str(e)
        print(message)
        print(e.args)

        return {'result': 'Error', 'message': message}
