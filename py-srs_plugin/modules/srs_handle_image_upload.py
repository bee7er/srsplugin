"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time
from c4d import documents
import sys, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

framesDir = srs_functions.get_plugin_directory(os.path.join('projects', 'frames'))
srsDomain = srs_functions.get_srs_domain()
teamToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, "teamToken")
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, "email")
userToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, "userToken")

# ===================================================================
def handle_image_upload(fileToUpload, submittedByUserUserToken, renderId):
# ===================================================================
    try:
        __modules__ = os.path.dirname(__file__)
        process_image_upload = os.path.join(__modules__, "srs_process_image_upload.py")

        p = subprocess.run([
            "python3",
            process_image_upload,
            email,
            userToken,
            fileToUpload,
            submittedByUserUserToken,
            framesDir,
            srsDomain,
            str(renderId),
            teamToken,
            ], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        #if None != p.stderr:
        #    raise Exception("Std err: " + p.stderr)

        return {'result': "OK", 'message': "Upload of image file " + fileToUpload + " completed"}

    except Exception as e:
        message = "Error trying to upload image. Error message: " + str(e)
        print(message)
        print(e.args)

        return {'result': 'Error', 'message': message}
