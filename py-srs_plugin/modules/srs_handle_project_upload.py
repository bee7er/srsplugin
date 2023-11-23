"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time
from c4d import documents
import sys, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

# Config settings
EMAIL = "email"
APITOKEN = "apiToken"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')
c4dProjectWithAssetsDir = srs_functions.get_plugin_directory(
    os.path.join('projects', 'with_assets', config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssetsDir'))
    )
srsDomain = srs_functions.get_srs_domain()
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, EMAIL)
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, APITOKEN)

# ===================================================================
def handle_project_upload(renderId):
# ===================================================================
    try:
        # Save the project with assets, to make sure it is up to date
        print("*** Saving project with assets to: ", c4dProjectWithAssetsDir)

        doc = documents.GetActiveDocument()
        missingAssets = []
        assets = []
        res = documents.SaveProject(
            doc,
            c4d.SAVEPROJECT_ASSETS | c4d.SAVEPROJECT_SCENEFILE,
            c4dProjectWithAssetsDir,
            assets,
            missingAssets
            )
        if True == res:
            print("*** Success saving project with assets")
        else:
            message = "*** Error saving project with assets to: " + c4dProjectWithAssetsDir
            print(message)
            return {'result': "Error", 'message': message}

        __modules__ = os.path.dirname(__file__)
        process_project_upload = os.path.join(__modules__, "srs_process_project_upload.py")

        p = subprocess.run([
            "python3",
            process_project_upload,
            c4dProjectWithAssets,
            c4dProjectWithAssetsDir,
            srsDomain,
            email,
            apiToken,
            str(renderId)
            ], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        return {'result': "OK", 'message': "Upload of project with assets file completed"}

    except Exception as e:
        message = "Error trying to upload project. Error message: " + str(e)
        print(message)
        print(e.args)

        return {'result': 'Error', 'message': message}
