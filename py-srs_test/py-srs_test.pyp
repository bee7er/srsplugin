"""
Kicks off testing a render submission

@see https://www.dataquest.io/blog/python-subprocess/

"""

import os, sys, c4d
from c4d import gui, bitmaps, utils, documents
# Import modules
__root__ = os.path.dirname(__file__)
if os.path.join(__root__, 'modules') not in sys.path: sys.path.insert(0, os.path.join(__root__, 'modules'))
import srs_handle_render

__res__ = c4d.plugins.GeResource()
__res__.Init(__root__)

# Settings
PYTHON_INTERPRETER = "python3"
COMMANDLINE_EXECUTABLE = "/Applications/Maxon Cinema 4D 2023/Commandline.app/Contents/MacOS/Commandline"

# TODO Unique ID can be obtained from www.plugincafe.com
PLUGIN_ID = 1046234
# Dialog elements
INFO_TEXT = 100011

class TestDlg(c4d.gui.GeDialog):
# ===================================================================

    def CreateLayout(self):
    # ===================================================================
        self.SetTitle("Test Render Submission")
        self.GroupBegin(id=110000, flags=c4d.BFH_SCALEFIT, cols=1, rows=2)
        self.AddStaticText(id=INFO_TEXT, flags=c4d.BFV_MASK, initw=145, name="Click OK to run test", borderstyle=c4d.BORDER_NONE)
        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
        self.GroupEnd()

        return True

    def Command(self, messageId, bc):
    # ===================================================================
        """ Called when the user clicks on the dialog """

        if messageId == c4d.DLG_OK:
            # Kick off the render job
            # srs_handle_render.handle_render(PYTHON_INTERPRETER, COMMANDLINE_EXECUTABLE)

            print("Using BatchRender to handle a render request")

            # Retrieves a list of all Cinema 4D files of this directory
            # os.listdir base its encoding on the passed encoding of the directory
            # so it's important to pass an unicode string.
            c4dFiles = list()

            projectsDir = self.get_plugin_directory('projects')

            print("Loading projects from: ", projectsDir)

            for file in os.listdir(projectsDir):
                if file.endswith(".c4d"):
                    c4dFiles.append(os.path.join(projectsDir, file))

            if not c4dFiles:
                raise RuntimeError("There is no Cinema 4D file in this directory.")

            # Retrieves the batch render instance
            br = c4d.documents.GetBatchRender()
            if br is None:
                raise RuntimeError("Failed to retrieve the batch render instance.")

            # Iterates the list of Cinema 4D paths and adds them in the BatchRender
            for file in c4dFiles:
                print("Adding: ", br.GetElementCount(), " with: ", file)
                res = br.AddFile(file, br.GetElementCount())
                if True == res:
                    print("Added successfully")
                else:
                    print("Add failed")

            print("Added to get count: ", br.GetElementCount())

            # Loops over the elements
            for i in range(br.GetElementCount()):
                # If the element is not finished, prints the path
                if br.GetElementStatus(i) != c4d.RM_FINISHED:
                    print(br.GetElement(i))
                else:
                    print("This one is finished: ", br.GetElement(i))

            print("Completed BatchRender load")

            # Opens the Batch Render
            # br.Open()
            # print("We Opened the batch renderer")

            br.SetRendering(c4d.BR_START)
            print("We kicked off the batch renderer")

        elif messageId == c4d.DLG_CANCEL:
            # Close the Dialog
            self.Close()

        return True


    def get_plugin_directory(self, dir):
    # ===================================================================
        # Returns the full path to the plugin directory, or a named subdirectory
        # pluginDir, _ = os.path.split(os.path.dirname(__file__))

        # print("Plugin dir: ", pluginDir)
        # print("Second dir: ", _)

        if '' != dir:
            return os.path.join(os.path.dirname(__file__), dir)

        return os.path.dirname(__file__)

class TestDlgCommand(c4d.plugins.CommandData):
# ===================================================================
    """ Class that holds the dialog instance """
    dialog = None

    def Execute(self, doc):
    # ===================================================================
        # Creates the dialog if its not already exists
        if self.dialog is None:
            self.dialog = TestDlg()

        # Opens the dialog
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=32)

    def RestoreLayout(self, sec_ref):
    # ===================================================================
        # Creates the dialog if it does not already exists
        if self.dialog is None:
            self.dialog = TestDlg()

        # Restores the layout
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

# ===================================================================
# main
# ===================================================================
if __name__ == "__main__":

    # Retrieves the icon path
    directory, _ = os.path.split(__file__)
    fn = os.path.join(directory, "res", "Icon_render.tif")

    # Creates a BaseBitmap
    bbmp = c4d.bitmaps.BaseBitmap()
    if bbmp is None:
        raise MemoryError("Failed to create a BaseBitmap.")

    # Init the BaseBitmap with the icon
    if bbmp.InitWith(fn)[0] != c4d.IMAGERESULT_OK:
        raise MemoryError("Failed to initialise the BaseBitmap.")

    # Registers the plugin
    c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID,
                                      str="Submit Render Test",
                                      info=0,
                                      help="Testing the creation of a subprocess",
                                      dat=TestDlgCommand(),
                                      icon=bbmp)
