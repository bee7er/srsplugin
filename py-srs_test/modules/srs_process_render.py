"""
A separate sript to invoke the shell script which renders the frames
"""
import os, sys, subprocess

# Params
input_params = sys.argv

def process_render(pluginDir=input_params[1], projectDir=input_params[2], rangeFrom=input_params[3], rangeTo=input_params[4]):
# ===================================================================
    try:
        res = subprocess.run([
            os.path.join(pluginDir, 'srs_render.sh'),
            '/Applications/Maxon Cinema 4D 2023/Commandline.app/Contents/MacOS/Commandline',
            projectDir,
            str(rangeFrom),
            str(rangeTo)
            ], capture_output=True, text=True)
        print(res)
        print("Std out: ", res.stdout)
        print("Std err: ", res.stderr)

    except Exception as e:
        message = "Error trying to render. Error message: " + str(e)
        print(message)
        print(e.args)

    print("Render completed")

# Invoke the process render function
if __name__=="__main__":
    process_render()

    print("COMPLETED: Render subprocess completed")