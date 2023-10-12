"""
Manages the render of one or more frames
"""
import c4d, os, time
import subprocess

def handle_render(pythonInterpreter, commandLineExecutable):
# ===================================================================
    # Submits a background job to render one or more frames

    try:
        print("Submitting render")

        pluginDir = get_plugin_directory('')
        modulesDir = get_plugin_directory('modules')
        projectDir = get_plugin_directory('projects')

        res = subprocess.run([
                pythonInterpreter,
                os.path.join(modulesDir, "srs_process_render.py"),
                commandLineExecutable,
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
    # Returns the full path to the plugin directory, or a named subdirectory
    pluginDir, _ = os.path.split(os.path.dirname(__file__))
    if '' != dir:
        return os.path.join(pluginDir, dir)

    return pluginDir