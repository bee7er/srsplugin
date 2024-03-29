"""
Copyright: Etheridge 2024
Author: Brian Etheridge

"""
import os, time
import sys, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_uploadProject.sh'
else:
    HANDLER = __root__ + '\srs_uploadProject.cmd'

# Config settings
TEAMTOKEN = "teamToken"
EMAIL = "email"
USERTOKEN = "userToken"

# Params
input_params = sys.argv

# ===================================================================
def process_project_upload(
    c4dProjectWithAssets=input_params[1],
    c4dProjectWithAssetsDir=input_params[2],
    srsDomain=input_params[3],
    email=input_params[4],
    userToken=input_params[5],
    renderId=input_params[6],
    teamToken=input_params[7]
    ):
# ===================================================================
    # Posting the project with assets file to master
    # .....................................................

    try:
        config = srs_functions.get_config_values()
        debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
        verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

        if True == verbose:
            print("Submitting project with assets upload script: ", HANDLER)
            print("Using: ", c4dProjectWithAssets, ", in ", c4dProjectWithAssetsDir)
            print("Email: ", email)
            print("Token: ", userToken)
            print("Handler: ", HANDLER)

        p = subprocess.run([
            HANDLER,
            c4dProjectWithAssets,
            c4dProjectWithAssetsDir,
            srsDomain,
            email,
            userToken,
            renderId,
            teamToken], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        #if None != p.stderr:
        #    raise Exception("Std err: " + p.stderr)

    except Exception as e:
        message = "Error trying to upload project. Error message: " + str(e)
        print(message)
        print(e.args)
        raise RuntimeError("Error processing project upload: " + message)


# Invoke the process render function
if __name__=="__main__":
    process_project_upload()

    print("COMPLETED: Project upload subprocess completed")
