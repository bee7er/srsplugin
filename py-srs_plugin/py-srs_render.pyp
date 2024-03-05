"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description:
    - Submit Render Request
	- Shared Render Service
"""

import os, sys, time

__root__ = os.path.dirname(__file__)
if os.path.join(__root__, 'modules') not in sys.path: sys.path.insert(0, os.path.join(__root__, 'modules'))

import c4d
from c4d import gui, bitmaps, utils
from c4d import documents

# SRS module for various shared funcrtions
import srs_functions, srs_functions_c4d, srs_handle_project_upload, srs_connections

__res__ = c4d.plugins.GeResource()
__res__.Init(__root__)

# TODO Unique ID can be obtained from www.plugincafe.com
PLUGIN_ID = 1047986
GROUP_ID = 100000

FRAME_RANGE_FROM_TEXT = 100011
EDIT_FRAME_RANGE_FROM_TEXT = 100012
FRAME_RANGE_TO_TEXT = 100013
EDIT_FRAME_RANGE_TO_TEXT = 100014
COMBO_TEXT = 100015
SELCOMBO_BUTTON = 100016
FRAME_RANGES_TEXT = 100017
EDIT_FRAME_RANGES_TEXT = 100018
OUTPUT_C4D_PROJECT_TEXT = 100019
OUTPUT_C4D_PROJECT = 100020
OUTPUT_FORMAT_TEXT = 100021
OUTPUT_FORMAT = 100022

PLEASE_SELECT = 0
OVERRIDE = 1
USESETTINGS = 2

# Parameters
CUSTOMFRAMERANGES = "customFrameRanges"
C4DPROJECTWITHASSETS = "c4dProjectWithAssets"
C4DPROJECTNAME = "c4dProjectName"
TEAMTOKEN = "teamToken"
EMAIL = "email"
USERTOKEN = "userToken"
FROM = "from"
OVERRIDESETTINGS = "overrideSettings"
RENDERDETAILID = "renderDetailId"
RENDERID = "renderId"
TO = "to"
OUTPUTFORMAT = "outputFormat"
OUTPUTFRAMES = "outputFrames"

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))
srsApi = config.get(srs_functions.CONFIG_SECTION, 'srsApi')

# ===================================================================
class RenderDlg(c4d.gui.GeDialog):
# ===================================================================

    c4dProjectWithAssetsDir = ''
    c4dProjectWithAssets = ''
    c4dProjectName = ''

    overrideSettings = 0
    customFrameRanges = ''
    rangeFrom = 0
    rangeTo = 0
    outputFormat = ''

    srs_functions.validate_directories(config)

    overrideSettings = config.get(srs_functions.CONFIG_RENDER_SECTION, 'overrideSettings')
    if '' == overrideSettings:
        overrideSettings = OVERRIDE
    overrideSettings = int(overrideSettings)

    customFrameRanges = config.get(srs_functions.CONFIG_RENDER_SECTION, 'customFrameRanges')

    # ===================================================================
    def CreateLayout(self):
    # ===================================================================
        """ Called when Cinema 4D creates the dialog """

        # Refresh the config values
        config = srs_functions.get_config_values()

        validationResult = srs_functions.validate_config(config)
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

            gui.MessageDialog("ERRORS IN CONFIGURATION ENVIRONMENT FILE: Please correct the following issues: \n" + errorMessages)

        # Get the project with assets path and name
        self.c4dProjectWithAssetsDir = srs_functions.get_plugin_directory(
            os.path.join('projects', 'with_assets', config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssetsDir'))
            )
        self.c4dProjectWithAssets = config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets')

        renderData = srs_functions_c4d.get_render_settings()
        self.rangeFrom = renderData[srs_functions.RANGE_FROM]
        self.rangeTo = renderData[srs_functions.RANGE_TO]
        self.outputFormat = renderData[srs_functions.OUTPUT_FORMAT]

        self.SetTitle("SRS Submit Render Request")

        self.GroupBegin(id=GROUP_ID, flags=c4d.BFH_SCALEFIT, cols=2, rows=4)
        """ C4D Project with Assets field """
        self.AddStaticText(id=OUTPUT_C4D_PROJECT_TEXT, flags=c4d.BFV_MASK, initw=145, name="Project with Assets: ", borderstyle=c4d.BORDER_NONE)
        self.AddStaticText(id=OUTPUT_C4D_PROJECT, flags=c4d.BFV_MASK, initw=220, name=self.c4dProjectWithAssets, borderstyle=c4d.BORDER_NONE)
        """ Use active render settings field """
        self.AddStaticText(id=COMBO_TEXT, flags=c4d.BFV_MASK, initw=145, name="Override active render settings: ", borderstyle=c4d.BORDER_NONE)
        self.AddComboBox(SELCOMBO_BUTTON, flags=c4d.BFH_LEFT, initw=160)
        self.AddChild(SELCOMBO_BUTTON, PLEASE_SELECT, 'Please select')
        self.AddChild(SELCOMBO_BUTTON, OVERRIDE, 'Override render settings')
        self.AddChild(SELCOMBO_BUTTON, USESETTINGS, 'Use render settings')
        self.SetInt32(SELCOMBO_BUTTON, self.overrideSettings)
        """ Custom ranges field """
        self.AddStaticText(id=FRAME_RANGES_TEXT, flags=c4d.BFV_MASK, initw=145, name="Custom frame ranges: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditText(EDIT_FRAME_RANGES_TEXT, c4d.BFV_MASK, initw=240, inith=16, editflags=0)
        self.SetString(EDIT_FRAME_RANGES_TEXT, self.customFrameRanges)
        """ Frame Range field """
        self.AddStaticText(id=FRAME_RANGE_FROM_TEXT, flags=c4d.BFV_MASK, initw=145, name="Frame range from: ", borderstyle=c4d.BORDER_NONE)
        self.AddStaticText(id=EDIT_FRAME_RANGE_FROM_TEXT, flags=c4d.BFV_MASK, initw=145, name=self.rangeFrom, borderstyle=c4d.BORDER_BLACK)
        self.AddStaticText(id=FRAME_RANGE_TO_TEXT, flags=c4d.BFV_MASK, initw=145, name="to: ", borderstyle=c4d.BORDER_NONE)
        self.AddStaticText(id=EDIT_FRAME_RANGE_TO_TEXT, flags=c4d.BFV_MASK, initw=145, name=self.rangeTo, borderstyle=c4d.BORDER_BLACK)
        """ Output Format field """
        self.AddStaticText(id=OUTPUT_FORMAT_TEXT, flags=c4d.BFV_MASK, initw=145, name="Output format: ", borderstyle=c4d.BORDER_NONE)
        self.AddStaticText(id=OUTPUT_FORMAT, flags=c4d.BFV_MASK, initw=145, name=self.outputFormat, borderstyle=c4d.BORDER_NONE)

		# Check if we are overriding render settings
        if OVERRIDE == self.overrideSettings:
            self.toggleEditableFields(True)
        else:
            self.toggleEditableFields(False)

        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
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
        # Refresh the config values
        config = srs_functions.get_config_values()

        # User click on Ok button
        if messageId == c4d.DLG_OK:

            if '' == srs_functions_c4d.get_project():
                gui.MessageDialog("Please open your project file and ensure your project with assets file is up to date.")
                return True

            validationResult = self.validate()
            if True == validationResult:
                self.overrideSettings = self.GetInt32(SELCOMBO_BUTTON)
                self.customFrameRanges = self.GetString(EDIT_FRAME_RANGES_TEXT)
                self.rangeFrom = self.GetString(EDIT_FRAME_RANGE_FROM_TEXT)
                self.rangeTo = self.GetString(EDIT_FRAME_RANGE_TO_TEXT)

                if True == verbose:
                    print("Form data passed validation")
                if True == debug:
                    print("Render requested")
                # Save to the config file
                srs_functions.update_config_values(srs_functions.CONFIG_RENDER_SECTION, [
                    ('overrideSettings', str(self.overrideSettings)),
                    ('outputFormat', self.outputFormat),
                    ('customFrameRanges', self.customFrameRanges)
                    ])

                if True == self.submitRenderRequest():
                    # Reset the range for the next submission
                    self.rangeFrom = 0
                    self.rangeTo = 0
                    if True == verbose:
                        teamToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, TEAMTOKEN)
                        email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, EMAIL)
                        userToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, USERTOKEN)

                        # Get and log the current status for this slave
                        responseData = srs_connections.submitRequest(
                            (srsApi + "/status"),
                            {TEAMTOKEN:teamToken, EMAIL:email, USERTOKEN:userToken}
                            )
                        if 'Error' == responseData['result']:
                            gui.MessageDialog("Error:\n" + responseData['message'])
                            return False

                        print("Current status: ", responseData['message'])

                    # Close the Dialog
                    self.Close()

                else:
                    print("Submission of render request cancelled")
                    return False

            else:
                if True == verbose:
                    print("Form data failed validation")
                errorMessages = sep = ""
                for error in validationResult:
                    errorMessages += sep + error
                    sep = "\n"

                gui.MessageDialog("ERROR IN FORM DATA: Please correct the following issues: \n" + errorMessages)

            return True

        # User click on Cancel button
        elif messageId == c4d.DLG_CANCEL:
            if True == verbose:
                print("User clicked Cancel")

            # Close the Dialog
            self.Close()
            return True

        # If the user opted to override the render settings, then allow access to the custom ranges field
        if self.overrideSettings != self.GetInt32(SELCOMBO_BUTTON):
            # Override option has changed
            if OVERRIDE == self.GetInt32(SELCOMBO_BUTTON):
                self.toggleEditableFields(True)

            else:
                self.toggleEditableFields(False)

            self.LayoutChanged(id=GROUP_ID)
            self.overrideSettings = self.GetInt32(SELCOMBO_BUTTON)

        return True

    # ===================================================================
    def toggleEditableFields(self, overridingRenderSettings):
    # ===================================================================
        """ Hides or shows the override fields
        """
        if True == overridingRenderSettings:
            self.HideElement(FRAME_RANGES_TEXT, False)
            self.HideElement(EDIT_FRAME_RANGES_TEXT, False)
            self.HideElement(FRAME_RANGE_FROM_TEXT, True)
            self.HideElement(EDIT_FRAME_RANGE_FROM_TEXT, True)
            self.HideElement(FRAME_RANGE_TO_TEXT, True)
            self.HideElement(EDIT_FRAME_RANGE_TO_TEXT, True)
        else:
            self.HideElement(FRAME_RANGES_TEXT, True)
            self.HideElement(EDIT_FRAME_RANGES_TEXT, True)
            self.HideElement(FRAME_RANGE_FROM_TEXT, False)
            self.HideElement(EDIT_FRAME_RANGE_FROM_TEXT, False)
            self.HideElement(FRAME_RANGE_TO_TEXT, False)
            self.HideElement(EDIT_FRAME_RANGE_TO_TEXT, False)

    # ===================================================================
    def submitRenderRequest(self):
    # ===================================================================
        """
        Submit the render request to the master node
        """
        # Validate the custom ranges if we are overriding settings

        # Refresh the config values
        config = srs_functions.get_config_values()

        self.c4dProjectName = srs_functions_c4d.get_projectName()

        print("self.overrideSettings=", self.overrideSettings)
        print("self.customFrameRanges=", self.customFrameRanges)
        print("self.rangeFrom=", self.rangeFrom)
        print("self.rangeTo=", self.rangeTo)

        if OVERRIDE == self.overrideSettings:
            # Analyse the custom frange ranges
            self.customFrameRanges = srs_functions.analyse_frame_ranges(self.customFrameRanges)
            if '' == self.customFrameRanges:
                if True == verbose:
                    print('customFrameRanges: ', self.customFrameRanges)
                gui.MessageDialog("Please enter at least one valid range, in the format 'm - m, n - n, etc'")
                return False

        # Get the user to confirm the submission
        framesToBeSubmitted = self.customFrameRanges
        if USESETTINGS == self.overrideSettings:
            framesToBeSubmitted = str(self.rangeFrom) + ' - ' + str(self.rangeTo)

        yesNo = gui.QuestionDialog(
            "Submitting frames: \n" + framesToBeSubmitted + "\n\n" +
            "Click Yes to submit the render request.\n\n"
            )
        if False == yesNo:
            return False

        sendData = {
            TEAMTOKEN:config.get(srs_functions.CONFIG_REGISTRATION_SECTION, TEAMTOKEN),
            EMAIL:config.get(srs_functions.CONFIG_REGISTRATION_SECTION, EMAIL),
            USERTOKEN:config.get(srs_functions.CONFIG_REGISTRATION_SECTION, USERTOKEN),
            OVERRIDESETTINGS:self.overrideSettings,
            CUSTOMFRAMERANGES:self.customFrameRanges,
            FROM:self.rangeFrom,
            TO:self.rangeTo,
            C4DPROJECTWITHASSETS:self.c4dProjectWithAssets,
            C4DPROJECTNAME:self.c4dProjectName,
            OUTPUTFORMAT:self.outputFormat,
        }
        if True == verbose:
            print("Sending data: ", sendData)

        responseData = srs_connections.submitRequest((srsApi + "/render"), sendData)
        if 'Error' == responseData['result']:
            gui.MessageDialog("Error:\n" + responseData['message'])
            return False

        # Upload the project with assets file
        srs_handle_project_upload.handle_project_upload(responseData[RENDERID])

        if True == verbose:
            print("Submit project with assets to master")

        if True == verbose:
            print("Render request record id: ", responseData[RENDERID])

        # if OVERRIDE == self.overrideSettings:
        #    gui.MessageDialog("Custom ranges submitted for render: " + self.customFrameRanges)
        # else:
        #    gui.MessageDialog("Range submitted for render: " + "\nFrom frame: " + str(self.rangeFrom) + "\nTo frame:" + str(self.rangeTo))

        return True

    # ===================================================================
    def validate(self):
    # ===================================================================
        """ Validate the submitted form
        Args:

        Returns:
            bool: True else an array of error messages.
        """
        validationResult = []

        if 0 == self.GetInt32(SELCOMBO_BUTTON):
            validationResult.append("The Override render settings field is required")

        if self.GetInt32(EDIT_FRAME_RANGE_TO_TEXT) < self.GetInt32(EDIT_FRAME_RANGE_FROM_TEXT):
            validationResult.append("The From Frame must be before the To Frame")

        if 0 == len(validationResult):
            return True

        return validationResult

# ===================================================================
class RenderDlgCommand(c4d.plugins.CommandData):
# ===================================================================
    """Command Data class that holds the RenderDlg instance."""
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
        # Creates the dialog if it does not already exists
        if self.dialog is None:
            self.dialog = RenderDlg()

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
            self.dialog = RenderDlg()

        # Restores the layout
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

# ===================================================================
# main
# ===================================================================
if __name__ == "__main__":
    if True == verbose:
        print("Setting up SRS Render Request Plugin")

    # Retrieves the icon path
    directory, _ = os.path.split(__file__)
    fn = os.path.join(directory, "res", "Icon_register.tif")

    # Creates a BaseBitmap
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp is None:
        raise MemoryError("Failed to create a BaseBitmap.")

    # Init the BaseBitmap with the icon
    if bmp.InitWith(fn)[0] != c4d.IMAGERESULT_OK:
        raise MemoryError("Failed to initialise the BaseBitmap.")

    # Registers the plugin
    c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID,
                                      str="SRS Submit Render Request",
                                      info=0,
                                      help="Submit render request",
                                      dat=RenderDlgCommand(),
                                      icon=bmp)

    if True == verbose:
        print("SRS Render Request Plugin set up ok")
