from . import operations as opx

# RESULT_FILES
# Standardized names for MIKE model result files (suffixed with format)
RESULT_FILE_TYPES = {
    "DEPTH_2D_ASC",
    "DEPTH_RIVER_ASC",
    "VELOCITY_2D_ASC",
    "DIRECTION_2D_ASC"
}

# PROCESSING_FILES
# Standardized names for files needed to postprocess results
PROCESSING_FILE_TYPES = {
    "MODEL_BOUNDARY_POLYGON",       # Boundary to clip model results to
    "DEPTH_RIVER_MASK_POLYGON"      # Polygon areas to be removed from DEPTH_RIVER
}

# OPERATION NAMES LINKED TO FUNCTION AND FILE_TYPES
# Should be a list in the form of [function reference, arg1, arg2, etc.]
# See operations.py for descriptions of each function

OPERATIONS = {
    "process2DDepth" : [opx.process2DDepth, "DEPTH_2D_ASC"],        
    "process2DVelocity" : [opx.process2DVelocity, "DEPTH_2D_ASC"],      
    "process2DDirection" : [opx.process2DDirection, "DEPTH_2D_ASC"],     
    "processRiverDepth" : [opx.processRiverDepth, "DEPTH_2D_ASC"],    
    "processFullDepth" : [opx.processFullDepth, "DEPTH_2D_ASC"],    
    "processClipDepth" : [opx.processClipDepth, "DEPTH_2D_ASC"],      
    "processClipVelocity" : [opx.processClipVelocity, "DEPTH_2D_ASC"],      
    "processClean" : [opx.processClean, "DEPTH_2D_ASC"],
    "OP_FOR_TESTING_ONLY" : [opx.FOR_TESTING_ONLY, "DEPTH_2D_ASC", "MODEL_BOUNDARY_POLYGON"]
}