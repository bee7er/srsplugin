"""
Copyright: Etheridge 2024
Author: Brian Etheridge

PLEASE NOTE:  These utility functions need c4d.
Put functions that do not need c4d into srs_functions.py

"""
import c4d, os, platform, srs_functions
from c4d import documents

__root__ = os.path.dirname(os.path.dirname(__file__))

RANGE_FROM = "RANGE_FROM"
RANGE_TO = "RANGE_TO"
RANGE_STEP = "RANGE_STEP"
FRAME_RATE = "FRAME_RATE"
OUTPUT_FORMAT = "OUTPUT_FORMAT"

# ===================================================================
def get_render_settings():
# ===================================================================
    # Gets render settings from the current active set
    # .....................................................

    activeDocument = c4d.documents.GetActiveDocument()
    renderData = activeDocument.GetActiveRenderData()

    # TODO add more output formats in the render settings
    # We must convert from the numeric output format
    # Define a dictionary that maps numeric values to file extensions
    format_to_extension = {
        1100: 'tif',
        1101: 'tga',
        1102: 'bmp',
        1103: 'iff',
        1104: 'jpg',
        1105: 'pict',
        1106: 'psd',
        1125: 'mp4',
        1023671: 'png',
        1073784596: 'mov',
        # Add more format-value-to-extension mappings as needed
    }
    # Use the dictionary to get the corresponding file extension
    output_format_value = int(renderData[c4d.RDATA_FORMAT]);

    if output_format_value in format_to_extension:
        output_extension = format_to_extension[output_format_value]

        # print("output_extension=", output_extension)

    else:
        output_extension = 'unknown'  # Handle unsupported or unknown values

        # print("*** unknown extension value=", output_format_value)

    return {
        RANGE_FROM: int(renderData[c4d.RDATA_FRAMEFROM].Get() * renderData[c4d.RDATA_FRAMERATE]),
        RANGE_TO: int(renderData[c4d.RDATA_FRAMETO].Get() * renderData[c4d.RDATA_FRAMERATE]),
        RANGE_STEP: renderData[c4d.RDATA_FRAMESTEP],
        FRAME_RATE: int(renderData[c4d.RDATA_FRAMERATE]),
        OUTPUT_FORMAT: output_extension,
    }

# ===================================================================
def get_project():
# ===================================================================
    # Gets project full path and name from the currently loaded project
    # .................................................................

    md = c4d.documents.GetActiveDocument()
    path = c4d.documents.BaseDocument.GetDocumentPath(md)
    c4dProjectFullPath = ''
    if '' == path:
        print("A project has not yet been opened")
    else:
        c4dProjectFullPath = os.path.join(path, c4d.documents.BaseDocument.GetDocumentName(md))
        print("NB Project opened is: ", c4dProjectFullPath)

    return c4dProjectFullPath

# ===================================================================
def get_projectName():
# ===================================================================
    # Gets project name from the currently loaded project
    # ...................................................

    md = c4d.documents.GetActiveDocument()
    if '' == md:
        print("A project has not yet been opened")
        return ''

    projectName = c4d.documents.BaseDocument.GetDocumentName(md)
    print("Project name is ", projectName)

    return projectName

# ===================================================================
def saveProjectWithAssets():
# ===================================================================
    # Saves the project with assets to the nominated directory
    # ........................................................
    try:
        config = srs_functions.get_config_values()
        debug = bool(int(config.get(srs_functions.CONFIG_SECTION, 'debug')))

        c4dProjectWithAssets = get_projectName()
        if '' == c4dProjectWithAssets:
            message = "A project has not yet been opened"
            print(message)
            return message
        if -1 == c4dProjectWithAssets.find('.c4d'):
            # Add the file extension, because when we save the file it will be created with a c4d extension
            c4dProjectWithAssets += '.c4d'

        # Directory is the same name as the project, without the extension
        c4dProjectWithAssetsDir = c4dProjectWithAssets.rsplit(".", 1)[0]
        c4dProjectWithAssetsDirFullPath = srs_functions.get_plugin_directory(os.path.join('projects', 'with_assets', c4dProjectWithAssetsDir))

        if True == debug:
            print("Saving project with assets " + c4dProjectWithAssets + ' to ' + c4dProjectWithAssetsDir)

        doc = documents.GetActiveDocument()
        missingAssets = []
        assets = []
        res = documents.SaveProject(
            doc,
            c4d.SAVEPROJECT_ASSETS | c4d.SAVEPROJECT_SCENEFILE,
            c4dProjectWithAssetsDirFullPath,
            assets,
            missingAssets
            )
        if True == res:
            if True == debug:
                print("Project with assets " + c4dProjectWithAssets + ' saved successfully to ' + c4dProjectWithAssetsDir)
            # Save project details to the config file
            srs_functions.update_config_values(
                srs_functions.CONFIG_SECTION,
                [(srs_functions.C4D_PROJECT_WITH_ASSETS_DIR, c4dProjectWithAssetsDir), (srs_functions.C4D_PROJECT_WITH_ASSETS, c4dProjectWithAssets)]
                )

            if True == debug:
                print("Plugin configuration details updated")

            return True

        else:
            message = "Error saving project with assets to: " + c4dProjectWithAssetsDir
            print(message)
            return message

    except Exception as e:
        message = "Error trying to save project with assets. Error message: " + str(e)
        print(message)
        print(e.args)

        return message

# ===================================================================
def get_ResultsOutputDirectory():
# ===================================================================
    # Gets the directory from the project settings
    # ............................................
    doc = documents.GetActiveDocument()
    activeRenderData = doc.GetActiveRenderData()
    if None == activeRenderData:
        raise RuntimeError("Failed to retrieve the active render data")
    # Check to see if we have a save path defined
    if "" == activeRenderData[c4d.RDATA_PATH]:
        raise RuntimeError("No save path has been defined")

    # Note how to resolve tokens in the render data
    savePath = c4d.modules.tokensystem.StringConvertTokens(activeRenderData[c4d.RDATA_PATH], rpData={'_doc': doc, '_rData': activeRenderData})
    # Check the save path exists
    if True != os.path.exists(savePath):
        os.mkdir(savePath)

    return savePath
