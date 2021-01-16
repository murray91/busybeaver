from . import operations as opx

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