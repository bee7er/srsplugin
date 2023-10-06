"""
Kicks off testing a render submission
"""

import os, sys, c4d
from c4d import gui, bitmaps, utils
# Import modules
__root__ = os.path.dirname(__file__)
if os.path.join(__root__, 'modules') not in sys.path: sys.path.insert(0, os.path.join(__root__, 'modules'))
import srs_handle_render

__res__ = c4d.plugins.GeResource()
__res__.Init(__root__)

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
            srs_handle_render.handle_render()

        elif messageId == c4d.DLG_CANCEL:
            # Close the Dialog
            self.Close()

        return True

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
