from . import operations as opx

# RESULT_FILES
# Standardized names for MIKE model result files (suffixed with format)
RESULT_FILE_TYPES = {
    "DFSU_REULTS_ANIMATED",     # animated dfsu results from MIKE
    "DFSU_RESULTS_MAX",         # max dfsu results from MIKE
    "DEPTH_2D_ASC",
    "DEPTH_RIVER_ASC",
    "VELOCITY_2D_ASC",
    "DIRECTION_2D_ASC"
}

# PROCESSING_FILES
# Standardized names for files needed to postprocess results
PROCESSING_FILE_TYPES = {
    "MODEL_BOUNDARY_POLYGON",       # Boundaries to clip model results to
    "DEPTH_RIVER_MASK_POLYGON",     # Polygon areas to be removed from DEPTH_RIVER
    "DFSU_RESULTS_DIRECTION",     # Output location for extractDirectionFromDfsu
}

# MODEL_PARAMETERS
# Standardized names for other model parameters which are not files
MODEL_PARAMETERS = {
    "MODEL_NAME", # Name/alias of the model
    "MODEL_PATH", # Path to model output folder
    "MODEL_GDB_PATH", # Path to the model's GDB
    "DIRECTION_TIMESTEP", # Integer timestep to extract direction from dfsu in model
    "2D_DEPTH_TIF_NAME", # Name of 2d depth raster (exclusing river) in tif format
    "2D_DEPTH_GDB_NAME", # Name of 2d depth raster (exclusing river) in gdb
    "2D_VELOCITY_GDB_NAME", # Name of 2d velocity raster (exclusing river) in gdb ... unclipped
    "2D_DIRECTION_GDB_NAME", # Name of 2d direction raster (excluding river) in gdb ... unclipped
    "RIVER_DEPTH_GDB_NAME", # Name of 2d river depth raster in gdb ... unclipped
    "FULL_DEPTH_GDB_NAME", # Name of full depth raster (2d and river merged) ... unclipped
    "FINAL_DEPTH_GDB_NAME", # Final name of depth raster after clipping
    "FINAL_VELOCITY_GDB_NAME", # Final name of velocity raster after clipping
    "FINAL_DIRECTION_GDB_NAME", # Final name of direction raster after clipping
    "CLIP_FIELD", # Name of column in attribute table of MODEL_BOUNDARY_POLYGON
    "CLIP_VALUE", # Value in CLIP_FIELD to use as clip olygon
    "CRS", # Coordinate system string for all rasters (e.g. 'ETRS 1989 UTM Zone 32N')
}

# OPERATION NAMES LINKED TO FUNCTION AND FILE_TYPES
# Should be a list in the form of [function reference, arg1, arg2, etc.]
# See operations.py for descriptions of each function

OPERATIONS = {
    "extractDirectionFromDfsu" :    [opx.extractDirectionFromDfsu, 
                                    "DFSU_REULTS_ANIMATED", "DFSU_RESULTS_DIRECTION", "DIRECTION_TIMESTEP"],
    "createGDB" : [opx.createGDB, "MODEL_GDB_PATH", "MODEL_NAME"], 
    "processASC_2DDepth" : [opx.ascToGDB, "DEPTH_2D_ASC", "MODEL_GDB_PATH", "2D_DEPTH_GDB_NAME"],    
    "processTIF_2DDepth" : [opx.dfsuToTif, "DFSU_RESULTS_MAX", "Maximum water depth", 0, "2D_DEPTH_TIF_NAME"],  
    "processASC_2DVelocity" : [opx.ascToGDB, "VELOCITY_2D_ASC", "MODEL_GDB_PATH", "2D_VELOCITY_GDB_NAME"],      
    "processASC_2DDirection" : [opx.ascToGDB, "DIRECTION_2D_ASC", "MODEL_GDB_PATH", "2D_DIRECTION_GDB_NAME"],     
    "processASC_RiverDepth" : [opx.ascToGDB, "DEPTH_RIVER_ASC", "MODEL_GDB_PATH", "RIVER_DEPTH_GDB_NAME"],        
    "processClipResults" : [opx.clipAllRasters, "MODEL_GDB_PATH", "MODEL_BOUNDARY_POLYGON",
                            "CLIP_FIELD", "CLIP_VALUE"],   
    "processCRS" : [opx.setCRS, "MODEL_GDB_PATH", "CRS"],  
    "processMergeRiver2DDepth" : [opx.mergeRasters, "2D_DEPTH_GDB_NAME", "RIVER_DEPTH_GDB_NAME", 
                                "FULL_DEPTH_GDB_NAME", "MODEL_GDB_PATH"],
    "processcleanRasters" : [opx.cleanRasters,  "MODEL_GDB_PATH", 
                                                "FULL_DEPTH_GDB_NAME", "2D_VELOCITY_GDB_NAME", "2D_DIRECTION_GDB_NAME",
                                                "FINAL_DEPTH_GDB_NAME", "FINAL_VELOCITY_GDB_NAME", "FINAL_DIRECTION_GDB_NAME"],
    "OP_FOR_TESTING_ONLY" : [opx.FOR_TESTING_ONLY, "DEPTH_2D_ASC", "MODEL_BOUNDARY_POLYGON"]
}