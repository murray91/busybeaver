# This file defines standard names for input files to be referenced in the config file

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