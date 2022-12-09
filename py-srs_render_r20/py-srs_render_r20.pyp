"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Description:
    - Submit Render Request
	- Shared Render Service
"""

import os, sys, time

__root__ = os.path.dirname(os.path.dirname(__file__))
if os.path.join(__root__, 'modules') not in sys.path: sys.path.insert(0, os.path.join(__root__, 'modules'))

import c4d
from c4d import gui, bitmaps, utils
# SRS module for various shared funcrtions
import srs_functions, srs_project_handler, srs_connections

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

PLEASE_SELECT = 0
OVERRIDE = 1
USESETTINGS = 2

# Parameters
CUSTOMFRAMERANGE = "custom_frame_range"
EMAIL = "email"
FROM = "from"
C4DPROJECTWITHASSETS = "c4dProjectWithAssets"
OVERRIDESETTINGS = "override_settings"
RENDERDETAILID = "render_detail_id"
RENDERID = "render_id"
TO = "to"

config = srs_functions.get_config_values()
debug = bool(config.get(srs_functions.CONFIG_SECTION, 'debug'))
srsApi = config.get(srs_functions.CONFIG_SECTION, 'srsApi')

class RenderDlg(c4d.gui.GeDialog):
    
    overrideSettings = 0
    customFrameRanges = ''
    rangeFrom = 0
    rangeTo = 0
             
    def CreateLayout(self):
        """ Called when Cinema 4D creates the dialog """

        # TODO Submissions aren't allowed if registration dialog is not open

        # Get the currently active render settings
        renderData = srs_functions.get_render_settings()

        self.rangeFrom = renderData[srs_functions.RANGE_FROM]
        self.rangeTo = renderData[srs_functions.RANGE_TO]
        
        # Initialise the form fields from the config file
        self.overrideSettings = int(config.get(srs_functions.CONFIG_RENDER_SECTION, 'overrideSettings'))
        
        self.SetTitle("Submit Trendman Render request")
		
        self.GroupBegin(id=GROUP_ID, flags=c4d.BFH_SCALEFIT, cols=2, rows=4)
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
        self.AddEditNumber(EDIT_FRAME_RANGE_FROM_TEXT, c4d.BFV_MASK, initw=80, inith=16)
        self.SetInt32(EDIT_FRAME_RANGE_FROM_TEXT, self.rangeFrom)
        self.AddStaticText(id=FRAME_RANGE_TO_TEXT, flags=c4d.BFV_MASK, initw=145, name="to: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditNumber(EDIT_FRAME_RANGE_TO_TEXT, c4d.BFV_MASK, initw=80, inith=16)
        self.SetInt32(EDIT_FRAME_RANGE_TO_TEXT, self.rangeTo)
		# Check if we are overriding render settings
        if OVERRIDE == self.overrideSettings:
            self.toggleEditableFields(True)
        else:
            self.toggleEditableFields(False)
            
        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
        self.GroupEnd()
        
        return True

    def Command(self, messageId, bc):
        """ Called when the user clicks on the dialog, clicks button, etc, or when a menu item selected.

        Args:
            messageId (int): The ID of the resource that triggered the event.
            bc (c4d.BaseContainer): The original message container.

        Returns:
            bool: False on error else True.
        """
        # User click on Ok button
        if messageId == c4d.DLG_OK:
            
            validationResult = self.validate()
            if True == validationResult:
                self.overrideSettings = self.GetInt32(SELCOMBO_BUTTON)
                self.customFrameRanges = self.GetString(EDIT_FRAME_RANGES_TEXT)
                self.rangeFrom = self.GetInt32(EDIT_FRAME_RANGE_FROM_TEXT)
                self.rangeTo = self.GetInt32(EDIT_FRAME_RANGE_TO_TEXT)
                
                if True == debug: 
                    print("Form data passed validation")
                    print("Submitting render request")
                # Save to the config file
                srs_functions.update_config_values(srs_functions.CONFIG_RENDER_SECTION, [('overrideSettings', str(self.overrideSettings))])
                
                if True == self.submitRenderRequest():
                    # Reset the range for the next submission
                    self.rangeFrom = 0
                    self.rangeTo = 0
                    # Close the Dialog
                    self.Close()

                else:
                    print("Submission of render request cancelled")
                    return False
            
            else:
                if True == debug: 
                    print("Form data failed validation")
                errorMessages = sep = ""
                for error in validationResult:
                    errorMessages += sep + error
                    sep = "\n"
                
                gui.MessageDialog("ERROR: Please correct the following issues: \n" + errorMessages)

            return True

        # User click on Cancel button
        elif messageId == c4d.DLG_CANCEL:
            if True == debug: 
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

    def toggleEditableFields(self, overridingRenderSettings):
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
        
    def submitRenderRequest(self):
        """ 
        Submit the render request to the master node

        NB Running these tests from srsplugin folder:
        
        Testing with curl on the command line:
		        curl -X POST -H "Content-Type: application/json" -d '{"sequence": "poipoi", "from": 8, "to": 88}' http://srsapi.test/api1/renders/request

        Testing upload to master:

                # Uploading rendered frames to master
                # NB we must use the vagrant directory sequence
                    curl -v -F 'upload=@/home/vagrant/Code/srstest/srs/redshifttest/tars/RedshiftTestBePngs.tar.gz' -H "Content-Type: multipart/form-data" http://srsapi.test/results

        Testing download from master:

                curl --output ./projects/RedshiftTestBePngs.tar.gz http://srsapi.test/uploads/projects/RedshiftTestBe.c4d

        """
        # First of all we upload the project with assets file to the server
        # TODO Check that the file exists
        yesNo = gui.QuestionDialog("Are you sure the project with assets file is up to date?")
        if False == yesNo:
            return False;
        # Go ahead and submit the render request, starting with the uploading of the project with assets file
        srs_project_handler.handle_project()

        # TODO Analyse and validate frame ranges
        ######ranges = srs_functions.analyse_frame_ranges("1 - 3,5-7,8, 10-7, a-5, 3.5 - 9, 155-88")
        ######print ranges        

        if True == debug:
            print("Submit project with assets to master")

        if True == debug:
            print("Render request going to: ", srsApi)

        sendData = {
            EMAIL:config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email'),
            C4DPROJECTWITHASSETS:config.get(srs_functions.CONFIG_SECTION, 'c4dProjectWithAssets'),
            OVERRIDESETTINGS:self.overrideSettings,
            CUSTOMFRAMERANGE:self.customFrameRanges,
            FROM:self.rangeFrom, 
            TO:self.rangeTo
        }
        if True == debug:
            print("Sending data: ", sendData)
        responseData = srs_connections. submitRequest(self, (srsApi + "render"), sendData)
        if 'Error' == responseData['result']:
            gui.MessageDialog("Error:\n" + responseData['message'])
            return False

        if True == debug:
            print("Render request record id: ", responseData[RENDERID])

        gui.MessageDialog("Range submitted for render: " + "\nFrom frame: " + str(self.rangeFrom) + "\nTo frame:" + str(self.rangeTo))
        
        return True


    def validate(self):
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

class RenderDlgCommand(c4d.plugins.CommandData):
    """Command Data class that holds the RenderDlg instance."""
    dialog = None
    
    def Execute(self, doc):
        """Called when the user executes a command via either CallCommand() or a click on the Command from the extension menu.

        Args:
            doc (c4d.documents.BaseDocument): The current active document.

        Returns:
            bool: True if the command success.
        """
        # Creates the dialog if its not already exists
        if self.dialog is None:
            self.dialog = RenderDlg()

        # Opens the dialog
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=32)

    def RestoreLayout(self, sec_ref):
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


# main
if __name__ == "__main__":
    if True == debug: 
        print "Submit Trendman Render request plugin"
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
                                      str="Shared Render Service",
                                      info=0,
                                      help="Submit render request",
                                      dat=RenderDlgCommand(),
                                      icon=bmp)
    
    if True == debug: 
        print "SRS Submit Render request registered ok"

