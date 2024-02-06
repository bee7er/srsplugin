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
    submittedByUserToken=input_params[4],
    renderId=input_params[5]
    ):
# ===================================================================
    # Downloading the project with assets file from master
    # .....................................................
    try:
        if True == verbose:
            print("Downloading handler: ", HANDLER)
            print("Downloading project with assets file to: ", downloadPWADir)
            print("Downloading project with assets dir to: ", c4dProjectWithAssets)
            print("Downloading project from user api token: ", submittedByUserToken)

        print("Downloading project for render Id: ", renderId)

        p = subprocess.run([
            HANDLER,
            c4dProjectWithAssets,
            downloadPWADir,
            srsDomain,
            submittedByUserToken,
            renderId], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        #if None != p.stderr:
        #    raise Exception("Std err: " + p.stderr)

    except Exception as e:
        message = "Error trying to download. Error message: " + str(e)
        print(message)
        print(e.args)
        raise RuntimeError("Error processing project download: " + message)

# Invoke the process render function
if __name__=="__main__":
    process_project_download()

    print("COMPLETED: Project download subprocess completed")
