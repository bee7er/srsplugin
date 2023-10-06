"""
Manages the render of one or more frames
"""
import c4d, os, time
import subprocess

def handle_render():
# ===================================================================
    # Submits a background job to render one or more frames

    try:
        print("Submitting render")

        __modules__ = os.path.dirname(__file__)

        pluginDir = get_plugin_directory('')
        projectDir = get_plugin_directory('projects')

        res = subprocess.run([
                "python3",
                os.path.join(__modules__, "srs_process_render.py"),
                '/Applications/Maxon Cinema 4D 2023/Commandline.app/Contents/MacOS/Commandline',
                pluginDir,
                projectDir,
                str(0),
                str(1)
            ], capture_output=True, text=True)
        print(res)
        print("Std out: ", res.stdout)
        print("Std err: ", res.stderr)

    except Exception as e:
        message = "Error trying to render. Error message: " + str(e)
        print(message)
        print(e.args)

    print("And we are back. Render submitted")

def get_plugin_directory(dir):
# ===================================================================
    # Returns the full path to the plugin directory
    pluginDir, _ = os.path.split(os.path.dirname(__file__))
    if '' != dir:
        return os.path.join(pluginDir, dir)

    return pluginDir