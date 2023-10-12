"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time
from c4d import documents
import sys, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_uploadProject.sh'
else:
    HANDLER = __root__ + '\srs_uploadProject.cmd'

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
def handle_project_upload():
# ===================================================================
    # Posting the project with assets file to master
    # .....................................................

    if True == verbose:
        print("*** Submitting project with assets upload script: ", HANDLER)
        print("*** Using: ", c4dProjectWithAssets, ", in ", c4dProjectWithAssetsDir)
        print("*** Email: ", email)
        print("*** Token: ", apiToken)
        print("*** Handler: ", HANDLER)

    try:
        '''
        # ##################
        # This section doesn't fail, but neither does the project get saved
        # It will create a new directory, but then puts nothing in it
        # Need to find out from the forum WTF this is doing

        # Save the project with assets, to make sure it is up to date
        print("*** Saving project with assets to: ", c4dProjectWithAssetsDir)
        missingAssets = []
        assets = []
        doc = documents.GetActiveDocument()

**** USE SAVEDOCUMENT RATHER THAN SAVEPROJECT - see handle_render function

        res = documents.SaveProject(doc, c4d.SAVEPROJECT_ASSETS | c4d.SAVEPROJECT_DONTTOUCHDOCUMENT | c4d.SAVEPROJECT_USEDOCUMENTNAMEASFILENAME | c4d.SAVEPROJECT_DONTFAILONMISSINGASSETS, c4dProjectWithAssetsDir, assets, missingAssets)
        if True == res:
            print("*** Success saving project with assets")
        else:
            print("*** Error saving project with assets")
        # print("Assets: ", ' '.join(map(str, assets)))
        # print("Missing Assets: ", ' '.join(map(str, missingAssets)))

        # ##################
        '''

        __modules__ = os.path.dirname(__file__)
        process_project_upload = os.path.join(__modules__, "srs_process_project_upload.py")

        p = subprocess.run(["python3", process_project_upload, c4dProjectWithAssets, c4dProjectWithAssetsDir, srsDomain, email, apiToken], capture_output=True, text=True)
        #print(p)
        #print("Std out: ", p.stdout)
        #print("Std err: ", p.stderr)

    except Exception as e:
        message = "Error trying to upload project. Error message: " + str(e)
        print(message)
        print(e.args)

    if True == verbose:
        print("Submission of project with assets file completed")