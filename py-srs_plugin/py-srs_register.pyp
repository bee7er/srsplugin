"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description:
    - Register as a slave node for group renders
	- Shared Render Service

"""

import os, sys, time
import subprocess

__root__ = os.path.dirname(__file__)
if os.path.join(__root__, 'modules') not in sys.path: sys.path.insert(0, os.path.join(__root__, 'modules'))

import c4d
from c4d import gui, bitmaps, utils
# SRS module for various shared functions
import srs_functions, srs_connections, srs_handle_project_download, srs_handle_image_upload, srs_handle_results_download, srs_handle_render

__res__ = c4d.plugins.GeResource()
__res__.Init(__root__)

# TODO Unique ID can be obtained from www.plugincafe.com
PLUGIN_ID = 1047985

TEAMTOKEN_TEXT = 100011
EDIT_TEAMTOKEN_TEXT = 100012
USERNAME_TEXT = 100013
EDIT_USERNAME_TEXT = 100014
COMBO_TEXT = 100015
SELCOMBO_BUTTON = 100016
NEWTEAM_BUTTON = 100017
BLANK = 100018

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
c4dProjectDir = srs_functions.get_plugin_directory('projects')
downloadPWADir = srs_functions.get_plugin_directory(os.path.join('projects', 'downloads'))
srsDomain = srs_functions.get_srs_domain()

# Config settings
AVAILABILITY = "availability"
TEAMTOKEN = "teamToken"
EMAIL = "email"
USERNAME = "userName"
USERTOKEN = "userToken"

# Parameters
ACTIONINSTRUCTION = "actionInstruction"
RENDERDETAILID = "renderDetailId"

# ===================================================================
class RegistrationDlg(c4d.gui.GeDialog):
# ===================================================================

    actionStatus = AS_READY
    renderDetailId = 0
    teamToken = ""
    email = ""
    userName = ""
    userToken = ""
    availability = 0
    statusBlock = None
    serverBlock = None
    counter = 0
    renderingData = {}

    # ===================================================================
    def CreateLayout(self):
    # ===================================================================
        """
            Called when Cinema 4D creates the dialog
        """

        # Refresh the config values
        config = srs_functions.get_config_values()
        validationResult = srs_functions.validate_environment(config)
        if True == validationResult:
            if True == verbose:
                print("Config values passed validation")
        else:
            if True == verbose:
                print("Config values failed validation")

            errorMessages = sep = ""
            for error in validationResult:
                errorMessages += sep + error
                sep = "\n"

            gui.MessageDialog("ERRORS IN CONFIGURATION FILE: Please correct the following issues: \n" + errorMessages)

        # Initialise the form fields from the config file
        self.teamToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, TEAMTOKEN)
        self.email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, EMAIL)
        self.userName = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, USERNAME)
        self.userToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, USERTOKEN)
        self.availability = int(config.get(srs_functions.CONFIG_REGISTRATION_SECTION, AVAILABILITY))
        self.SetTitle("SRS Register Render Availability")

        self.GroupBegin(id=110000, flags=c4d.BFH_SCALEFIT, cols=3, rows=4)
        """ Team Token field """
        self.AddStaticText(id=TEAMTOKEN_TEXT, flags=c4d.BFV_MASK, initw=145, name="Team Token: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditText(EDIT_TEAMTOKEN_TEXT, c4d.BFV_MASK, initw=240, inith=16, editflags=0)
        self.SetString(EDIT_TEAMTOKEN_TEXT, self.teamToken)
        self.AddButton(id=NEWTEAM_BUTTON, flags=c4d.BFH_RIGHT | c4d.BFV_CENTER, initw=100, inith=16, name="New Team")

        """ User name field """
        self.AddStaticText(id=USERNAME_TEXT, flags=c4d.BFV_MASK, initw=145, name="User name: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditText(EDIT_USERNAME_TEXT, c4d.BFV_MASK, initw=240, inith=16, editflags=0)
        self.SetString(EDIT_USERNAME_TEXT, self.userName)
        self.AddStaticText(id=BLANK, flags=c4d.BFV_MASK, initw=145, name="", borderstyle=c4d.BORDER_NONE)

        """ Availability field """
        self.AddStaticText(id=COMBO_TEXT, flags=c4d.BFV_MASK, initw=145, name="Availability: ", borderstyle=c4d.BORDER_NONE)
        self.AddComboBox(SELCOMBO_BUTTON, flags=c4d.BFH_LEFT, initw=160)
        self.AddChild(SELCOMBO_BUTTON, PLEASE_SELECT, 'Please select')
        self.AddChild(SELCOMBO_BUTTON, AVAILABLE, 'Available for renders')
        self.AddChild(SELCOMBO_BUTTON, UNAVAILABLE, 'Unavailable for renders')
        self.SetInt32(SELCOMBO_BUTTON, self.availability)
        self.AddStaticText(id=BLANK, flags=c4d.BFV_MASK, initw=145, name="", borderstyle=c4d.BORDER_NONE)

        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
        self.GroupEnd()

        self.GroupBegin(id=120000, flags=c4d.BFH_SCALEFIT, cols=1, rows=1)
        self.statusBlock=self.AddCustomGui(1000100, c4d.CUSTOMGUI_HTMLVIEWER, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 300, 300, c4d.BaseContainer())
        statusText = '<div style="width:100%;height=:100%;">Local platform: <b>' + srs_functions.get_platform() + '</b></div>'
        statusText += '<div style="width:100%;height=:100%;">Remote server: <b>' + srsDomain + '</b></div>'
        if True == debug:
            statusText += '<div style="width:100%;height=:100%;">Running debug: <b>YES</b></div>'
        self.statusBlock.SetText(statusText)
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

            # Set the plugin ready to accept instructions
            self.actionStatus = AS_READY
            print("Ready as starting state")

            if True == verbose:
                print("User clicked Ok")

            # >>>>>>>>>> Place test section from test_process_project.py here.  Also import that module above.

            validationResult = self.validate()
            if True == validationResult:
                self.teamToken = self.GetString(EDIT_TEAMTOKEN_TEXT)
                self.userName = self.GetString(EDIT_USERNAME_TEXT)
                self.availability = self.GetInt32(SELCOMBO_BUTTON)
                # Save to the config file
                srs_functions.update_config_values(
                    srs_functions.CONFIG_REGISTRATION_SECTION,
                    [(TEAMTOKEN, self.teamToken), (EMAIL, self.email), (USERNAME, self.userName), (AVAILABILITY,  str(self.availability))]
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
                print("Cancelled registration")

            # End Timer function
            self.SetTimer(0)

            # Close the Dialog
            self.Close()
            return True

        # User click on Cancel button
        elif messageId == NEWTEAM_BUTTON:
            if True == verbose:
                print("User clicked New Team")

            validationResult = self.validate()
            if True == validationResult:
                self.teamToken = self.GetString(EDIT_TEAMTOKEN_TEXT)
                self.userName = self.GetString(EDIT_USERNAME_TEXT)
                self.availability = self.GetInt32(SELCOMBO_BUTTON)
                # Save to the config file
                srs_functions.update_config_values(
                    srs_functions.CONFIG_REGISTRATION_SECTION,
                    [(TEAMTOKEN, self.teamToken), (EMAIL, self.email), (USERNAME, self.userName), (AVAILABILITY,  str(self.availability))]
                    )
                if True == verbose:
                    print("Form data passed validation")

                # Create a new team with the API
                teamToken = self.createNewTeam()
                # Error, exit
                if False == teamToken:
                    return False

                gui.MessageDialog("New team created")
                self.teamToken = teamToken
                srs_functions.update_config_values(
                    srs_functions.CONFIG_REGISTRATION_SECTION,
                    [(TEAMTOKEN, self.teamToken)]
                    )
                self.SetString(EDIT_TEAMTOKEN_TEXT, self.teamToken)

            else:
                if True == verbose:
                    print("Form data failed validation")

                errorMessages = sep = ""
                for error in validationResult:
                    errorMessages += sep + error
                    sep = "\n"

                gui.MessageDialog("ERROR: Please correct the following issues: \n" + errorMessages)

        return True

    # ===================================================================
    def validate(self):
    # ===================================================================
        """
            Validate the submitted form
        """
        validationResult = []

        # Preprocess form fields
        self.SetString(EDIT_TEAMTOKEN_TEXT, self.GetString(EDIT_TEAMTOKEN_TEXT).replace("\\", ''))
        self.SetString(EDIT_USERNAME_TEXT, self.GetString(EDIT_USERNAME_TEXT).replace("\\", ''))

        if "" == self.GetString(EDIT_TEAMTOKEN_TEXT).strip():
            validationResult.append("The team token field is required")

        if "" == self.GetString(EDIT_USERNAME_TEXT).strip():
            validationResult.append("The user name field is required")

        if 0 == self.GetInt32(SELCOMBO_BUTTON):
            validationResult.append("The Availability field is required")

        if 0 == len(validationResult):
            return True

        return validationResult

    # ===================================================================
    def submitRegistrationRequest(self):
    # ===================================================================

        sendData = {
            TEAMTOKEN: self.teamToken,
            EMAIL: self.email,
            USERNAME: self.userName,
            USERTOKEN: self.userToken,
            AVAILABILITY: self.availability,
        }
        responseData = srs_connections.submitRequest((srsApi + "/register"), sendData)
        if 'Error' == responseData['result']:
            gui.MessageDialog("Error:\n" + responseData['message'])
            return False

        return True

    # ===================================================================
    def createNewTeam(self):
    # ===================================================================

        sendData = {
            EMAIL: self.email,
            USERTOKEN: self.userToken
        }
        responseData = srs_connections.submitRequest((srsApi + "/new_team"), sendData)
        if 'Error' == responseData['result']:
            gui.MessageDialog("Error:\n" + responseData['message'])
            return False

        return responseData['newTeamToken'];

    # ===================================================================
    def Timer(self, msg):
    # ===================================================================
        """
            This method is called automatically by Cinema 4D according to the timer set with GeDialog.SetTimer method.

        Args:
            msg (c4d.BaseContainer): The timer message
        """
        if True == debug:
            print("Action status: ", self.actionStatus)

        if AS_READY == self.actionStatus:
            if AVAILABLE == self.availability:
                if True == debug:
                    print("Available")
                self.renderingData = srs_connections.submitRequest((srsApi + "/available"), {TEAMTOKEN:self.teamToken, EMAIL:self.email, USERTOKEN:self.userToken})

                if 'Error' != self.renderingData['result'] and AI_DO_RENDER == self.renderingData[ACTIONINSTRUCTION]:

                    # Download the project with assets file
                    result = srs_handle_project_download.handle_project_download(
                        self.renderingData['c4dProjectWithAssets'],
                        self.renderingData['submittedByUserToken'],
                        self.renderingData['renderId']
                        )

                    if 'Error' == result['result']:
                        print("Error in project download: ", self.renderingData['message'])
                        return

                    # Do render in the background
                    self.renderDetailId = self.renderingData[RENDERDETAILID]
                    self.actionStatus = AS_RENDERING
                    # Kick off the render job
                    srs_handle_render.handle_render(
                        c4dProjectDir,
                        downloadPWADir,
                        self.renderingData['c4dProjectWithAssets'],
                        self.renderingData['c4dProjectName'],
                        self.renderingData['from'],
                        self.renderingData['to'],
                        self.renderingData['submittedByUserToken'],
                        self.renderingData['renderId']
                        )

                if 'Error' == self.renderingData['result']:
                    print("Error in available: ", self.renderingData['message'])
                    return

        elif AS_RENDERING == self.actionStatus:
            if True == debug:
                print("Rendering")

            # We do not need to keep telling the master that we are rendering, so this bit is commented out
            ##responseData = srs_connections.submitRequest((srsApi + "/rendering"), {TEAMTOKEN:self.teamToken, EMAIL:self.email, USERTOKEN:self.userToken})
            ##if 'Error' == responseData['result']:
            ##    print("Error in rendering: ", responseData['message'])
            ##    return

            # Check if the frame images are available
            imageSavePath = srs_functions.get_plugin_directory(os.path.join('projects', 'frames'))
            # It is essential to sort the list in alphabetical order to ensure we don't
            # hit the end until all entries have been processed
            fileList = os.listdir(imageSavePath);
            fileList.sort();
            for file in fileList:

                if file.endswith(self.renderingData['outputFormat']):
                    # Upload image to server

                    fileFullPath = os.path.join(imageSavePath, file)

                    print("Uploading image. From team: ",
                        self.teamToken,
                        ", email: ",
                        self.email,
                        ", userToken: ",
                        self.userToken,
                        ", file: ",
                         fileFullPath,
                        " and submmit atoken: ",
                        self.renderingData['submittedByUserToken']
                        )

                    result = srs_handle_image_upload.handle_image_upload(
                        fileFullPath,
                        self.renderingData['submittedByUserToken'],
                        self.renderingData['renderId']
                        )

                    if 'Error' == result['result']:
                        print("Error in project download: ", self.renderingData['message'])
                        return

                    # Remove image from frames directory
                    os.remove(fileFullPath)

                if str(self.renderingData['to']) in file:
                    print('Ok we have finished: ', str(self.renderingData['to']))

                    if True == debug:
                        print(".....................................")
                        print("*** Completed rendering of this chunk")
                        print(".....................................")
                    # Back to ready for this slave
                    self.actionStatus = AS_READY

                    responseData = srs_connections.submitRequest(
                            (srsApi + "/complete"),
                            {TEAMTOKEN:self.teamToken, EMAIL:self.email, RENDERDETAILID:self.renderDetailId, USERTOKEN:self.userToken}
                        )
                    if 'Error' == responseData['result']:
                        print("Error in complete: ", responseData['message'])
                        return

                    # We are done
                    break

        # We always send an AWAKE message to the master
        if True == debug:
            print("Awake")
        responseData = srs_connections.submitRequest((srsApi + "/awake"), {TEAMTOKEN:self.teamToken, EMAIL:self.email, USERTOKEN:self.userToken})

        if 'Error' != responseData['result']:
            if AI_DO_DOWNLOAD == responseData[ACTIONINSTRUCTION]:

                # Download the rendered frames
                result = srs_handle_results_download.handle_results_download(responseData['frameDetails'])

                if 'OK' == result['result']:
                    gui.MessageDialog("Render download completed successfully")
                    return

            elif AI_DO_DISPLAY_OUTSTANDING == responseData[ACTIONINSTRUCTION]:
                # Details of outstanding renders have been returned
                self.counter = self.counter + 1
                self.statusBlock.SetText(
                    '<div style="text-align: right;margin-right: 15px;">Refresh count: ' +
                    str(self.counter) +
                    "</div>" +
                    responseData['submissionsAndRenders']
                    );

        if 'Error' == responseData['result']:
            print("Error in timer from API call: ", responseData['message'])
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
        # Creates the dialog if it does not already exists
        if self.dialog is None:
            self.dialog = RegistrationDlg()

        # Restores the layout
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

# ===================================================================
# main
# ===================================================================
if __name__ == "__main__":
    if True == verbose:
        print("Setting up SRS Register Plugin")

    # Retrieves the icon path
    directory, _ = os.path.split(__file__)
    fn = os.path.join(directory, "res", "Icon_render.tif")

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
        print("SRS Register Plugin set up ok")
