"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import c4d, os, time
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
c4dProjectWithAssetsDir = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssetsDir')
srsDomain = config.get(srs_functions.CONFIG_SECTION, 'srsDomain')
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, EMAIL)
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, APITOKEN)

# ===================================================================
def handle_project_upload():
# ===================================================================
    # Posting the project with assets file to master
    # .....................................................

    if True == verbose:
        print("*** Submitting project with assets upload script: ", HANDLER, ", with ", c4dProjectWithAssets, ", in ", c4dProjectWithAssetsDir)
        print("*** Email: ", email)
        print("*** Token: ", apiToken)
        print("*** Handler: ", HANDLER)

    try:

        p = subprocess.Popen([HANDLER, c4dProjectWithAssets, c4dProjectWithAssetsDir, srsDomain, email, apiToken], stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(p.stderr.read())
        print(p.stdout.read())
        p.communicate()

        print('*********************** success')
    except Exception as err:
        print(err.args)
        print('*********************** problem')

    print('*********************** done in upload handler')

    if True == verbose:
        print("Submission of project with assets file completed")