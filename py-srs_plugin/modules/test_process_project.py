"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Test section which can be put into py-srs_register.pyp to test the upload/download of the project zip
            # ///////////////////////////////
            __root_ = os.path.dirname(__file__)
            process_project = os.path.join(__root__, "modules", "test_process_project.py")

            print(process_project)

            p = subprocess.run([
                "python3",
                process_project,
                "sss@sss.com",
                "coiucoiuoiuoiuf983798df8d9879d",
                "coiucoiuoiuoiuf983798df8d9879d",
                "coiucoiuoiuoiuf983798df8d9879d",
                "coiucoiuoiuoiuf983798df8d9879d",
                "159"], capture_output=True, text=True)

            print("Std out: ", p.stdout)
            print("Std err: ", p.stderr)

            return False
            # //////////////////////////////////

"""
import os, time
import sys, subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

# Config settings
EMAIL = "email"
APITOKEN = "apiToken"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
input_params = sys.argv

# ===================================================================
def t_process_project_upload():
# ===================================================================
    # Posting the project with assets file to master
    # .....................................................

    try:
        # ///////////////////////////////
        __root__ = os.path.dirname(os.path.dirname(__file__))
        process_project = os.path.join(__root__, "test_uploadProject.sh")


        print("Running: ", process_project)
        print("Root: ", process_project)

        p = subprocess.run([
            process_project,
            "ssdfsdf",
            "gdgdfgdfg",
            "rgerbeberb",
            "sgdfgdfgdfg",
            "dssdfsdfsdf",
            str(159)
            ], capture_output=True, text=True)

        print("Std out: ", p.stdout)
        print("Std err: ", p.stderr)

        process_project = os.path.join(__root__, "test_downloadProject.sh")

        print("Running 2: ", process_project)

        p = subprocess.run([
            process_project,
            "ssdfsdf",
            "gdgdfgdfg",
            "rgerbeberb",
            "sgdfgdfgdfg",
            "dssdfsdfsdf",
            str(159)
            ], capture_output=True, text=True)

        print("Std out: ", p.stdout)
        print("Std err: ", p.stderr)

        # //////////////////////////////////

    except Exception as e:
        message = "Error trying to upload project. Error message: " + str(e)
        print(message)
        print(e.args)
        raise RuntimeError("*** Error processing project upload: " + message)


# Invoke the process render function
if __name__=="__main__":
    t_process_project_upload()

    print("COMPLETED: Project upload subprocess completed")
