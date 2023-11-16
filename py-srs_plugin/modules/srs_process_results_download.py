"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

"""
import os, sys, time, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

if srs_functions.OS_MAC == srs_functions.get_platform():
    HANDLER = __root__ + '/srs_downloadResults.sh'
else:
    HANDLER = __root__ + '\srs_downloadResults.cmd'

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
input_params = sys.argv

# ===================================================================
def process_results_download(
    c4dProjectWithAssets=input_params[1],
    frameDetail=input_params[2],
    outputToFramesDir=input_params[3],
    srsDomain=input_params[4],
    apiToken=input_params[5],
    renderId=input_params[6]
    ):
# ===================================================================
    # Downloading the results files from master
    # ..........................................
    try:
        p = subprocess.run([
            HANDLER,
            c4dProjectWithAssets,
            frameDetail,
            outputToFramesDir,
            srsDomain,
            apiToken,
            renderId], capture_output=True, text=True)

        if True == debug:
            if '' != p.stdout:
                print("Std out: ", p.stdout)
            if '' != p.stderr:
                print("Std err: ", p.stderr)

        #if None != p.stderr:
        #    raise Exception("Std err: " + p.stderr)

    except Exception as e:
        message = "Error trying to process download results. Error message: " + str(e)
        print(message)
        print(e.args)
        raise RuntimeError("*** Error processing results download: " + message)

# Invoke the process render function
if __name__=="__main__":
    process_results_download()

    print("COMPLETED: Results download subprocess completed")
