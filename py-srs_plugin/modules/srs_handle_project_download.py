"""
Copyright: Etheridge 2024
Author: Brian Etheridge

"""
import c4d, os, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadProject.sh'
else:
    HANDLER = __root__ + '\srs_downloadProject.cmd'

# ===================================================================
def handle_project_download(
    c4dProjectWithAssets,
    submittedByUserUserToken,
    renderId
    ):
# ===================================================================
    # Downloading the project with assets file from master
    # .....................................................
    try:
        config = srs_functions.get_config_values()
        debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
        verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
        downloadPWADir = srs_functions.get_plugin_directory(os.path.join('projects', 'downloads'))
        srsDomain = srs_functions.get_srs_domain()

        __modules__ = os.path.dirname(__file__)
        process_project_download = os.path.join(__modules__, "srs_process_project_download.py")

        print("Downloading handler: ", HANDLER, " with renderId: ", renderId)

        if True == verbose:
            print("Downloading handler: ", HANDLER)
            print("Downloading project with assets file to: ", downloadPWADir)
            print("Downloading project with assets dir to: ", c4dProjectWithAssets)
            print("Downloading project from user api token: ", submittedByUserUserToken)

        p = subprocess.run(["python3", process_project_download,
            c4dProjectWithAssets,
            downloadPWADir,
            srsDomain,
            submittedByUserUserToken,
            str(renderId)], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        #if None != p.stderr:
        #    raise Exception("Std err: " + p.stderr)

        return {'result': "OK", 'message': "Download of project with assets file completed"}

    except Exception as e:
        message = "Error trying to download. Error message: " + str(e)
        print(message)
        print(e.args)

        return {'result': 'Error', 'message': message}
