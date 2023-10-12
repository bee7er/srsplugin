"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import os, sys, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadProject.sh'
else:
    HANDLER = __root__ + '\srs_downloadProject.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
input_params = sys.argv

# ===================================================================
def process_project_download(
    c4dProjectWithAssets=input_params[1],
    downloadPWADir=input_params[2],
    srsDomain=input_params[3],
    submittedByUserApiToken=input_params[4]
    ):
# ===================================================================
    # Downloading the project with assets file from master
    # .....................................................
    try:
        if True == verbose:
            print("*** Downloading handler: ", HANDLER)
            print("*** Downloading project with assets file to: ", downloadPWADir)
            print("*** Downloading project with assets dir to: ", c4dProjectWithAssets)
            print("*** Downloading project from user api token: ", submittedByUserApiToken)

        p = subprocess.run([
            HANDLER,
            c4dProjectWithAssets,
            downloadPWADir,
            srsDomain,
            submittedByUserApiToken], capture_output=True, text=True)
        #print(p)
        #print("Std out: ", p.stdout)
        #print("Std err: ", p.stderr)

        if True == verbose:
            print("Download of project with assets file completed")

        return {'result': "OK", 'message': "Download of project with assets file completed"}

    except Exception as e:
        message = "Error trying to download. Error message: " + str(e)
        print(message)
        return {'result': 'Error', 'message': message}

# Invoke the process render function
if __name__=="__main__":
    process_project_download()

    print("COMPLETED: Project download subprocess completed")
