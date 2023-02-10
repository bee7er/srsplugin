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
PLUGIN_ID = 1047985

EMAIL_TEXT = 100011
EDIT_EMAIL_TEXT = 100012
COMBO_TEXT = 100013
SELCOMBO_BUTTON = 100014

PLEASE_SELECT = 0
AVAILABLE = 1
UNAVAILABLE = 2

# Action status is the status of this running plugin
AS_READY = "ready"
AS_RENDERING = "rendering"
# Action instructions are given by the master
AI_DO_RENDER = "render"
AI_DO_DOWNLOAD = "download"
AI_DO_DISPLAY_OUTSTANDING = "outstanding"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
srsApi = config.get(srs_functions.CONFIG_SECTION, 'srsApi')
c4dProjectDir = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectDir')
downloadPWADir = config.get(srs_functions.CONFIG_SECTION, 'downloadPWADir')

# Config settings
AVAILABILITY = "availability"
EMAIL = "email"
APITOKEN = "apiToken"

# Parameters
ACTIONINSTRUCTION = "actionInstruction"
RENDERDETAILID = "renderDetailId"

# ===================================================================
class RegistrationDlg(c4d.gui.GeDialog):
# ===================================================================

    actionStatus = AS_READY
    renderDetailId = 0
    email = ""
    apiToken = ""
    availability = 0
    statusBlock = None
    counter = 0

    # ===================================================================
    def CreateLayout(self):
    # ===================================================================
        """
            Called when Cinema 4D creates the dialog
        """

        # Refresh the config values
        config = srs_functions.get_config_values()

        # Initialise the form fields from the config file
        self.email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, EMAIL)
        self.apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, APITOKEN)
        self.availability = int(config.get(srs_functions.CONFIG_REGISTRATION_SECTION, AVAILABILITY))
        self.SetTitle("SRS Register Render Availability")
		
        self.GroupBegin(id=110000, flags=c4d.BFH_SCALEFIT, cols=2, rows=4)
        """ Email field """
        self.AddStaticText(id=EMAIL_TEXT, flags=c4d.BFV_MASK, initw=145, name="Email: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditText(EDIT_EMAIL_TEXT, c4d.BFV_MASK, initw=240, inith=16, editflags=0)
        self.SetString(EDIT_EMAIL_TEXT, self.email)

        """ Availability field """
        self.AddStaticText(id=COMBO_TEXT, flags=c4d.BFV_MASK, initw=145, name="Availability: ", borderstyle=c4d.BORDER_NONE)
        self.AddComboBox(SELCOMBO_BUTTON, flags=c4d.BFH_LEFT, initw=160)
        self.AddChild(SELCOMBO_BUTTON, PLEASE_SELECT, 'Please select')
        self.AddChild(SELCOMBO_BUTTON, AVAILABLE, 'Available for renders')
        self.AddChild(SELCOMBO_BUTTON, UNAVAILABLE, 'Unavailable for renders')
        self.SetInt32(SELCOMBO_BUTTON, self.availability)

        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
        self.GroupEnd()

        self.GroupBegin(id=120000, flags=c4d.BFH_SCALEFIT, cols=1, rows=1)
        self.statusBlock=self.AddCustomGui(1000099, c4d.CUSTOMGUI_HTMLVIEWER, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 300, 300, c4d.BaseContainer())
        self.statusBlock.SetText('<div style="width:100%;height=:100%;">Running system: ' + srs_functions.get_platform() + '</div>')
        self.GroupEnd()

        return True

    # ===================================================================
    def Command(self, messageId, bc):
    # ===================================================================
        """ Called when the user clicks on the dialog, clicks button, etc, or when a menu item selected.

        Args:
            messageId (int): The ID of the resource that triggered the event.
            bc (c4d.BaseContainer): The original message container.

        Returns:
            bool: False on error else True.
        """
        # User click on Ok button
        if messageId == c4d.DLG_OK:
            if True == verbose:
                print("User clicked Ok")
            
            validationResult = self.validate()
            if True == validationResult:
                self.email = self.GetString(EDIT_EMAIL_TEXT)
                self.availability = self.GetInt32(SELCOMBO_BUTTON)
                # Save to the config file
                srs_functions.update_config_values(
                    srs_functions.CONFIG_REGISTRATION_SECTION, [(EMAIL, self.email), (AVAILABILITY,  str(self.availability))]
                    )
                if True == verbose:
                    print("Form data passed validation")

                # Register availability with the API
                if True == self.submitRegistrationRequest():
                    # Dialog needs to stay open to handle communications
                    gui.MessageDialog("Registered OK. Leave the dialog open for background operations.")
                    
                    # Kick off the heartbeat Timer function
                    self.SetTimer(2000)

                else:
                    return False
            
            else:
                if True == verbose:
                    print("Form data failed validation")
                    
                errorMessages = sep = ""
                for error in validationResult:
                    errorMessages += sep + error
                    sep = "\n"
                    
                gui.MessageDialog("ERROR: Please correct the following issues: \n" + errorMessages)
                
            return True

        # User click on Cancel button
        elif messageId == c4d.DLG_CANCEL:
            if AS_RENDERING == self.actionStatus:
                yesNo = gui.QuestionDialog("You are currently rendering in the background.\nAre you sure you want to exit?")
                if False == yesNo:
                    if True == verbose:
                        print("Not cancelling after all")
                    return False;

            if True == debug: 
                print("*** Cancelled registration")

            # Close the Dialog
            self.Close()
            return True

        return True

    # ===================================================================
    def validate(self):
    # ===================================================================
        """
            Validate the submitted form
        """
        validationResult = []

        # Preprocess form fields
        self.SetString(EDIT_EMAIL_TEXT, self.GetString(EDIT_EMAIL_TEXT).replace("\\", ''))
            
        if "" == self.GetString(EDIT_EMAIL_TEXT).strip():
            validationResult.append("The Email field is required")
            
        if 0 == self.GetInt32(SELCOMBO_BUTTON):
            validationResult.append("The Availability field is required")
        
        if 0 == len(validationResult): 
            return True

        return validationResult

    # ===================================================================
    def submitRegistrationRequest(self):
    # ===================================================================
        
        sendData = {
            EMAIL: self.email,
            APITOKEN: self.apiToken,
            AVAILABILITY: self.availability,
        }
        responseData = srs_connections.submitRequest(self, (srsApi + "/register"), sendData)
        if 'Error' == responseData['result']:
            gui.MessageDialog("Error:\n" + responseData['message'])
            return False
        
        return True

    # ===================================================================
    def Timer(self, msg):
    # ===================================================================
        """
            This method is called automatically by Cinema 4D according to the timer set with GeDialog.SetTimer method.

        Args:
            msg (c4d.BaseContainer): The timer message
        """
        if AS_READY == self.actionStatus:
            if AVAILABLE == self.availability:
                if True == debug:
                    print "*** Available"
                responseData = srs_connections.submitRequest(self, (srsApi + "/available"), {EMAIL:self.email, APITOKEN:self.apiToken})

                if 'Error' != responseData['result'] and AI_DO_RENDER == responseData[ACTIONINSTRUCTION]:
                    # Download the project with assets file
                    result = srs_project_download_handler.handle_project_download(responseData['c4dProjectWithAssets'])

                    if 'Error' == result['result']:
                        print "Error in project download: ", responseData['message']
                        return

                    # Do render in the background
                    self.renderDetailId = responseData[RENDERDETAILID]
                    self.actionStatus = AS_RENDERING
                    # Kick off the render job
                    srs_render_handler.handle_render(
                        c4dProjectDir,
                        downloadPWADir,
                        responseData['c4dProjectWithAssets'],
                        responseData['from'],
                        responseData['to'],
                        responseData['outputFormat'],
                        )

                if 'Error' == responseData['result']:
                    print "Error in available: ", responseData['message']
                    return

        elif AS_RENDERING == self.actionStatus:
            if True == debug: 
                print "*** Rendering"

            # We do not need to keep telling the master that we are rendering
            ##responseData = srs_connections.submitRequest(self, (srsApi + "/rendering"), {EMAIL:self.email, APITOKEN:self.apiToken})
            ##if 'Error' == responseData['result']:
            ##    print "Error in rendering: ", responseData['message']
            ##    return

            # Check if the render has completed OK
            if True == os.path.exists(c4dProjectDir + "/actionCompleted.txt"):
                if True == debug:
                    print "xxxxxxxxxxxxxxxxxxxx"
                    print "*** Completed render"
                    print "xxxxxxxxxxxxxxxxxxxx"
                # Back to ready for this slave
                self.actionStatus = AS_READY

                responseData = srs_connections.submitRequest(self, (srsApi + "/complete"),
                        {EMAIL:self.email, RENDERDETAILID:self.renderDetailId, APITOKEN:self.apiToken}
                    )
                if 'Error' == responseData['result']:
                    print "Error in complete: ", responseData['message']
                    return

        # We always send an AWAKE message to the master
        if True == debug:
            print "*** Awake"
        responseData = srs_connections.submitRequest(self, (srsApi + "/awake"), {EMAIL:self.email, APITOKEN:self.apiToken})

        if 'Error' != responseData['result']:
            if AI_DO_DOWNLOAD == responseData[ACTIONINSTRUCTION]:
                # Download the rendered frames/psds
                result = srs_results_download_handler.handle_results_download(responseData['frameRanges'])

                if 'OK' == result['result']:
                    gui.MessageDialog("Render download completed successfully")
                    return

            elif AI_DO_DISPLAY_OUTSTANDING == responseData[ACTIONINSTRUCTION]:
                # Details of outstanding renders have been returned
                self.counter = self.counter + 1
                self.statusBlock.SetText('<div style="text-align: right;margin-right: 15px;">Refresh count: ' + str(self.counter) + "</div>" + responseData['submissionsAndRenders']);

        if 'Error' == responseData['result']:
            print "Error in timer from API call: ", responseData['message']
            return

# ===================================================================
class RegistrationDlgCommand(c4d.plugins.CommandData):
# ===================================================================
    """Command Data class that holds the RegistrationDlg instance."""
    dialog = None

    # ===================================================================
    def Execute(self, doc):
    # ===================================================================
        """Called when the user executes a command via either CallCommand() or a click on the Command from the extension menu.

        Args:
            doc (c4d.documents.BaseDocument): The current active document.

        Returns:
            bool: True if the command success.
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
    if True == verbose:
        print "Registering SRS Plugin"
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
    if True == debug: 
        print "*** SRS registered ok"