"""
Copyright: Etheridge Family Oct 2023
Author: Brian Etheridge

"""
import os, time
import sys, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_uploadImage.sh'
else:
    HANDLER = __root__ + '\srs_uploadImage.cmd'

# Config settings
EMAIL = "email"
APITOKEN = "apiToken"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
input_params = sys.argv

# ===================================================================
def process_image_upload(
    email=input_params[1],
    apiToken=input_params[2],
    fileToUpload=input_params[3],
    submittedByUserApiToken=input_params[4],
    framesDir=input_params[5],
    srsDomain=input_params[6],
    renderId=input_params[7]
    ):
# ===================================================================
    # Posting the project with assets file to master
    # .....................................................

    if True == verbose:
        print("*** Submitting project with assets upload script: ", HANDLER)
        print("*** Using: ", email, ", and token ", apiToken)
        print("*** File: ", fileToUpload)
        print("*** Submitter: ", submittedByUserApiToken)
        print("*** Handler: ", HANDLER)

    try:
        p = subprocess.run([
            HANDLER,
            email,
            apiToken,
            fileToUpload,
            submittedByUserApiToken,
            framesDir,
            srsDomain,
            renderId], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        #if None != p.stderr:
        #    raise Exception("Std err: " + p.stderr)

    except Exception as e:
        message = "Error trying to upload image. Error message: " + str(e)
        print(message)
        print(e.args)
        raise RuntimeError("*** Error processing image upload: " + message)

# Invoke the process render function
if __name__=="__main__":
    process_image_upload()

    print("COMPLETED: Image upload subprocess completed")
