"""
Copyright: Etheridge Family Nov 2022
Author: Brian Etheridge
"""
import c4d, os, platform

try:
    # R2023
    import configparser as configurator
    print("Running 2023")
except:
    # Prior to R2023
    import ConfigParser as configurator
    print("Running prior version to 2023")

__root__ = os.path.dirname(os.path.dirname(__file__))

RANGE_FROM = "RANGE_FROM"
RANGE_TO = "RANGE_TO"
RANGE_STEP = "RANGE_STEP"
FRAME_RATE = "FRAME_RATE"
OUTPUT_FORMAT = "OUTPUT_FORMAT"

OS_MAC = 'mac'
OS_UNKNOWN = 'unknown'
OS_WINDOWS = 'windows'

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
    # Gets project path and name from the currently loaded project
    # .....................................................

    md = c4d.documents.GetActiveDocument()
    fp = c4d.documents.BaseDocument.GetDocumentPath(md)
    c4dProject = ''
    if '' == fp:
        print("*** A project has not been opened")
    else:
        c4dProject = fp + '/' + c4d.documents.BaseDocument.GetDocumentName(md)
        print("Project opened is: ", c4dProject)

    return c4dProject
