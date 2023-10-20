"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge

Command line rendering:
        NB Since R21 you have to login to the command line to state from where the licence is coming:
        Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

        In the rendering process on the command line, one gets:

            Error running authentication: No License Model defined [license_impl.cpp(146)]
            ----
            Enter the license method:
              1) Maxon App
              2) Maxon Account
              3) Maxon License Server
              4) RLM
              Q) Quit
            Please select: 1
            License okay.

        Following this initialisation of the licence on the command line the render plugin worked
"""
import c4d, os, time
from c4d import gui
from c4d import documents
import subprocess
import srs_functions

__root__ = os.path.dirname(os.path.dirname(__file__))

config = srs_functions.get_config_values()
debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))
verbose = bool(int(config.get(srs_functions.CONFIG_SECTION, 'verbose')))

# Params
email = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'email')
apiToken = config.get(srs_functions.CONFIG_REGISTRATION_SECTION, 'apiToken')
srsDomain = srs_functions.get_srs_domain()

# ===================================================================
def handle_render(
    c4dProjectDir,
    downloadPWADir,
    c4dProjectWithAssets,
    rangeFrom,
    rangeTo,
    submittedByUserApiToken
    ):
# ===================================================================
    # Submits a render request for one or more frames to the BatchRender queue
    # ........................................................................

    if True == verbose:
        print("Processing c4dProjectWithAssets: ", downloadPWADir, '/', c4dProjectWithAssets, ' from: ', rangeFrom, ' to: ', rangeTo)

    try:
        print("Adding an entry to BatchRender queue")

        # Load the project
        projectDocumentPath = os.path.join(downloadPWADir, c4dProjectWithAssets)
        projectDocument = documents.LoadDocument(projectDocumentPath, c4d.SCENEFILTER_ONLY_RENDERDATA)
        if None != projectDocument:
            print('Successfully loaded projectDocument')
        else:
            raise RuntimeError('Failed to load project: ', os.path.join(downloadPWADir, c4dProjectWithAssets))

        # Set the chunk frame range in this instance of the project
        renderData = projectDocument.GetActiveRenderData()
        renderData[c4d.RDATA_FRAMEFROM] = c4d.BaseTime(rangeFrom, renderData[c4d.RDATA_FRAMERATE])
        renderData[c4d.RDATA_FRAMETO] = c4d.BaseTime(rangeTo, renderData[c4d.RDATA_FRAMERATE])
        # Set the save path
        savePath = srs_functions.get_plugin_directory(os.path.join('projects', 'frames', c4dProjectWithAssets))
        if True == debug:
            print("*** Setting save path to: ", savePath)

        print("*** Setting save path to: ", savePath)

        renderData[c4d.RDATA_PATH] = savePath

        # Update the project with the new details
        projectDocument.InsertRenderDataLast(renderData)

        res = documents.SaveDocument(projectDocument, projectDocumentPath, c4d.SAVEDOCUMENTFLAGS_CRASHSITUATION | c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT)
        if True == res:
            if True == debug:
                print("*** Success saving project with assets")

        else:
            raise RuntimeError("*** Error saving project with assets")

        # Retrieve the batch render instance
        br = c4d.documents.GetBatchRender()
        if br is None:
            raise RuntimeError("Failed to retrieve the batch render instance.")

        # Add the project to the end of the queue
        br.AddFile(projectDocumentPath, br.GetElementCount())

        # Start processing the render queue
        br.SetRendering(c4d.BR_START)
        if True == debug:
            print("*** Render queue started")

        return {'result': "OK", 'message': "Render of image files completed"}

    except Exception as e:
        message = "Error trying to render. Error message: " + str(e)
        print(message)
        print(e.args)

        return {'result': 'Error', 'message': message}
