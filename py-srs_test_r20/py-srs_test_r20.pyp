"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description:
    - Register as a slave node
	- Shared Render Service

"""

import os, sys, time

__root__ = os.path.dirname(os.path.dirname(__file__))
if os.path.join(__root__, 'modules') not in sys.path: sys.path.insert(0, os.path.join(__root__, 'modules'))

import c4d
from c4d import gui, bitmaps, utils
# SRS module for various shared funcrtions
import srs_functions, srs_connections, srs_project_download_handler, srs_results_download_handler, srs_render_handler

__res__ = c4d.plugins.GeResource()
__res__.Init(__root__)

# TODO Unique ID can be obtained from www.plugincafe.com
PLUGIN_ID = 1047987

# ===================================================================
class RegistrationDlg(c4d.gui.GeDialog):
# ===================================================================

    # ===================================================================
    def CreateLayout(self):
    # ===================================================================
        """
            Called when Cinema 4D creates the dialog
        """
        view=self.AddCustomGui(1000099, c4d.CUSTOMGUI_HTMLVIEWER, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 300, 300, c4d.BaseContainer())
        view.SetUrl("http://3n3.477.mywebsitetransfer.com/renders?selectedUserId=1", c4d.URL_ENCODING_UTF16)
        #view.SetText("We use cookies to give you the best online experience. By continuing to browse the site you are agreeing to our use of cookies.")

        self.Open(dlgtpye=1)

        return True

    # ===================================================================
    def Command(self, messageId, bc):
    # ===================================================================
        """ Called when the user clicks on the dialog, clicks button, etc, or when a menu item selected.
        """

        return True

# ===================================================================
class RegistrationDlgCommand(c4d.plugins.CommandData):
# ===================================================================
    """Command Data class that holds the RegistrationDlg instance."""
    dialog = None

    # ===================================================================
    def Execute(self, doc):
    # ===================================================================
        """Called when the user executes a command via either CallCommand() or a click on the Command from the extension menu.
        """
        # Creates the dialog if its not already exists
        if self.dialog is None:
            self.dialog = RegistrationDlg()

        # Opens the dialog
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=32)

    # ===================================================================
    def RestoreLayout(self, sec_ref):
    # ===================================================================
        """Used to restore an asynchronous dialog that has been placed in the users layout.

        Args:
            sec_ref (PyCObject): The data that needs to be passed to the dialog.

        Returns:
            bool: True if the restore success
        """
        # Creates the dialog if its not already exists
        if self.dialog is None:
            self.dialog = RegistrationDlg()

        # Restores the layout
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

# ===================================================================
# main
# ===================================================================
if __name__ == "__main__":

    # Retrieves the icon path
    directory, _ = os.path.split(__file__)
    fn = os.path.join(directory, "res", "Icon.tif")

    # Creates a BaseBitmap
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp is None:
        raise MemoryError("Failed to create a BaseBitmap.")

    # Init the BaseBitmap with the icon
    if bmp.InitWith(fn)[0] != c4d.IMAGERESULT_OK:
        raise MemoryError("Failed to initialise the BaseBitmap.")

    # Registers the plugin
    c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID,
                                      str="SRS Register Availability for Renders",
                                      info=0,
                                      help="Register your availability with SRS",
                                      dat=RegistrationDlgCommand(),
                                      icon=bmp)