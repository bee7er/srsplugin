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
import srs_functions, srs_connections, srs_render_handler

__res__ = c4d.plugins.GeResource()
__res__.Init(__root__)

# TODO Unique ID can be obtained from www.plugincafe.com
PLUGIN_ID = 1047985

EMAIL_TEXT = 100011
EDIT_EMAIL_TEXT = 100012
IP_TEXT = 100013
EDIT_IP_TEXT = 100014
COMBO_TEXT = 100015
SELCOMBO_BUTTON = 100016

PLEASE_SELECT = 0
AVAILABLE = 1
UNAVAILABLE = 2

# Action status is the status of this running plugin
AS_READY = "ready"
AS_RENDERING = "rendering"
# Action instructions are given by the master
AI_DO_RENDER = "render"

config = srs_functions.get_config_values()
debug = bool(config.get(srs_functions.CONFIG_SECTION, 'debug'))
srsApi = "http://srsapi.test/api1/"
#####srsApi = "https://3n3.477.mywebsitetransfer.com/api1/"

class RegistrationDlg(c4d.gui.GeDialog):

    actionStatus = AS_READY
    email = ""
    ipAddress = ""
    availability = 0
    
    def CreateLayout(self):
        """
            Called when Cinema 4D creates the dialog
        """
        # Initialise the form fields from the config file
        self.email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
        self.ipAddress = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'ipAddress')
        self.availability = int(config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'availability'))
        
        self.SetTitle("Register with SRS")
		
        self.GroupBegin(id=100000, flags=c4d.BFH_SCALEFIT, cols=2, rows=4)        
        """ Email field """
        self.AddStaticText(id=EMAIL_TEXT, flags=c4d.BFV_MASK, initw=145, name="Email: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditText(EDIT_EMAIL_TEXT, c4d.BFV_MASK, initw=240, inith=16, editflags=0)
        self.SetString(EDIT_EMAIL_TEXT, self.email)

        """ IP field """
        self.AddStaticText(id=IP_TEXT, flags=c4d.BFV_MASK, initw=145, name="IP Address: ", borderstyle=c4d.BORDER_NONE)
        self.AddEditText(EDIT_IP_TEXT, c4d.BFV_MASK, initw=240, inith=16, editflags=0)
        self.SetString(EDIT_IP_TEXT, self.ipAddress)

        """ Availability field """
        self.AddStaticText(id=COMBO_TEXT, flags=c4d.BFV_MASK, initw=145, name="Availability: ", borderstyle=c4d.BORDER_NONE)
        self.AddComboBox(SELCOMBO_BUTTON, flags=c4d.BFH_LEFT, initw=160)
        self.AddChild(SELCOMBO_BUTTON, PLEASE_SELECT, 'Please select')
        self.AddChild(SELCOMBO_BUTTON, AVAILABLE, 'Available for renders')
        self.AddChild(SELCOMBO_BUTTON, UNAVAILABLE, 'Unavailable for renders')
        self.SetInt32(SELCOMBO_BUTTON, self.availability)
		
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
            if True == debug: 
                print("User clicked Ok")
            
            validationResult = self.validate()
            if True == validationResult:
                self.email = self.GetString(EDIT_EMAIL_TEXT)
                self.ipAddress = self.GetString(EDIT_IP_TEXT)
                self.availability = self.GetInt32(SELCOMBO_BUTTON)
                # Save to the config file
                srs_functions.update_config_values(
                    srs_functions.CONFIG_REGISTRATION_SECTION, [('email', self.email), ('ipAddress', self.ipAddress), ('availability',  str(self.availability))]
                    )
                if True == debug: 
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

        return True

    def validate(self):
        """
            Validate the submitted form
        """
        validationResult = []
            
        if "" == self.GetString(EDIT_EMAIL_TEXT).strip():
            validationResult.append("The Email field is required")
        
        ip = self.GetString(EDIT_IP_TEXT).strip()
        if "" == ip:
            validationResult.append("The IP Address field is required")
        elif True != self.is_valid_ip(ip):
            validationResult.append("The IP Address is invalid")
            
        if 0 == self.GetInt32(SELCOMBO_BUTTON):
            validationResult.append("The Availability field is required")
        
        if 0 == len(validationResult): 
            return True

        return validationResult

    def is_valid_ip(self, ip):
        # TODO needs a better way to validate IP, and support IPv6
        elements = ip.split('.')
        if 4 != len(elements):
            return False
        
        for elem in elements:
            if True != elem.isdigit():
                return False
            
            if 0 > int(elem) or 255 < int(elem):
                return False
                
        return True
        
    def submitRegistrationRequest(self):
        
        sendData = {
            "email": self.email,
            "ipAddress": self.ipAddress,
            "availability": self.availability,
        }
        responseData = srs_connections.submitRequest(self, (srsApi + "register"), sendData)
        if 'Error' == responseData['result']:
            gui.MessageDialog("Error:\n" + responseData['message'])
            return False
        
        return True

    def Timer(self, msg):
        """
            This method is called automatically by Cinema 4D according to the timer set with GeDialog.SetTimer method.

        Args:
            msg (c4d.BaseContainer): The timer message
        """
        if AS_READY == self.actionStatus:
            if AVAILABLE == self.availability:
                if True == debug:
                    print "Available for team render instructions"
                responseData = srs_connections.submitRequest(self, (srsApi + "available"), { "email":"contact_bee@yahoo.com" })
                if AI_DO_RENDER == responseData['actionInstruction']:
                    self.actionStatus = AS_RENDERING
                    # Kick off the render job
                    srs_render_handler.handle_render()
            else:
                if True == debug:
                    print "Awake but not available"
                responseData = srs_connections.submitRequest(self, (srsApi + "awake"), { "email":"contact_bee@yahoo.com" })

            if 'Error' == responseData['result']:
                gui.MessageDialog("Error:\n" + responseData['message'])

        elif AS_RENDERING == self.actionStatus:
            if True == debug: 
                print "Rendering"
            responseData = srs_connections.submitRequest(self, (srsApi + "rendering"), {"email":"contact_bee@yahoo.com"})
            if 'Error' == responseData['result']:
                gui.MessageDialog("Error:\n" + responseData['message'])

            # Check if the render has completed OK
            if True == os.path.exists("/Users/brianetheridge/Code/srstest/actionCompleted.txt"):
                if True == debug:
                    print "Completed render"
                    print "TODO send the results to master"
                # Back to ready for this slave
                self.actionStatus = AS_READY
                responseData = srs_connections.submitRequest(self, (srsApi + "complete"), {"email":"contact_bee@yahoo.com"})
                if 'Error' == responseData['result']:
                    gui.MessageDialog("Error:\n" + responseData['message'])
          
class RegistrationDlgCommand(c4d.plugins.CommandData):
    """Command Data class that holds the RegistrationDlg instance."""
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
            self.dialog = RegistrationDlg()

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
            self.dialog = RegistrationDlg()

        # Restores the layout
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


# main
if __name__ == "__main__":
    if True == debug: 
        print "Registering SRS plugin"
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
                                      help="Register your availability with SRS",
                                      dat=RegistrationDlgCommand(),
                                      icon=bmp)
    if True == debug: 
        print "SRS registered ok"