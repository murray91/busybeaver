import logging
import os
import busybeaver.processes as proc

logging.basicConfig(filename='bb.log', filemode='w', format='%(asctime)s - %(levelname)s: %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

class Hut:
    """
    Main class for setting up single/batch post processing

    Usage example:
    process_manager = Hut()
    """
    def __init__(self):
      
        logging.info("Created new Hut.")
        self.models = []

    # Make huts iterable over models in self.models
    def __getitem__(self, index):
        if isinstance(index, str):
            for model in self.models:
                if model.name == index:
                    return model
        else:
            return self.models[index]

    def __len__(self):
        return len(self.models)

    def __iter__(self):
        return(HutIterator(self))

    def __next__(self):
        pass

    # sets the same parameter for many models to a value
    def setAll(self, param, value):
        for model in self.models:
            model.params[param] = value
    
    def runAll(self):
        logging.info("Starting to run processs for all models.")
        for model in self.models:
            logging.info("Running processs for {}...".format(model.name))
            for proc in model.runstack:
                proc.run()
        logging.info("Finished running processes for all models.")

# Allows iterating over Hut to get models      
class HutIterator:

    def __init__(self, hut):
        self.hut = hut
        self._index = 0

    def __next__(self):
        if self._index < len(self.hut.models):
            result = self.hut.models[self._index]
            self._index += 1
            return result
        raise StopIteration

class Model:
    """
    A class for holding information related to a single model

    Usage example:
    cool_model = Model("Name of model")

    """
    def __init__(self, model_name):
        
        logging.info("Created model: {}.".format(model_name))
        self.name = model_name
        self.runstack = []
        self.params = {
                "DFSU_REULTS_ANIMATED" : None,     # animated dfsu results from MIKE
                "DFSU_RESULTS_MAX" : None,         # max dfsu results from MIKE
                "DFSU_RESULTS_DIRECTION" : None,   # Output location for extractDirectionFromDfsu
                "DEPTH_2D_ASC" : None,             # MIKE 2d max depth in asc format
                "DEPTH_RIVER_ASC" : None,          # MIKE river max depth in asc format
                "VELOCITY_2D_ASC" : None,          # MIKE 2d max velocity in asc format
                "DIRECTION_2D_ASC" : None,         # MIKE 2d direction in asc format
                "MODEL_BOUNDARY_POLYGON" : None,   # Boundaries to clip model results to
                "MODEL_GDB_PATH" : None,           # Path to the model's GDB (with .gdb extension)
                "DIRECTION_TIMESTEP" : None,       # Integer timestep to extract direction from dfsu in model
                "2D_DEPTH_TIF_NAME" : None,        # Name of 2d depth raster (exclusing river) in tif format
                "2D_DEPTH_GDB_NAME" : None,        # Name of 2d depth raster (exclusing river) in gdb
                "2D_VELOCITY_GDB_NAME" : None,     # Name of 2d velocity raster (exclusing river) in gdb ... unclipped
                "2D_DIRECTION_GDB_NAME" : None,    # Name of 2d direction raster (excluding river) in gdb ... unclipped
                "RIVER_DEPTH_GDB_NAME" : None,     # Name of 2d river depth raster in gdb ... unclipped
                "FULL_DEPTH_GDB_NAME" : None,      # Name of full depth raster (2d and river merged) ... unclipped
                "FINAL_DEPTH_GDB_NAME" : None,     # Final name of depth raster after clipping
                "FINAL_VELOCITY_GDB_NAME" : None,  # Final name of velocity raster after clipping
                "FINAL_DIRECTION_GDB_NAME" : None, # Final name of direction raster after clipping
                "CLIP_FIELD" : None,               # Name of column in attribute table of MODEL_BOUNDARY_POLYGON
                "CLIP_VALUE" : None,               # Value in CLIP_FIELD to use as clip olygon
                "CRS" : None,                      # Coordinate system string for all rasters (e.g. 'ETRS 1989 UTM Zone 32N')
        }

        # defaults
        self.params["2D_DEPTH_GDB_NAME"] = "{}_2d_dep".format(self.name)
        self.params["2D_VELOCITY_GDB_NAME"] = "{}_2d_vel".format(self.name)
        self.params["2D_DIRECTION_GDB_NAME"] = "{}_2d_dir".format(self.name)
        self.params["RIVER_DEPTH_GDB_NAME"] = "{}_riv_dep".format(self.name)
        self.params["FULL_DEPTH_GDB_NAME"] = "{}_full_dep".format(self.name)
        self.params["FINAL_DEPTH_GDB_NAME"] = "{}_Depth".format(self.name)
        self.params["FINAL_VELOCITY_GDB_NAME"] = "{}_Velocity".format(self.name)
        self.params["FINAL_DIRECTION_GDB_NAME"] = "{}_Direction".format(self.name)

    # Adds a raw python function and arguments to runstack
    def addProcess(self, name, func, *args):
        logging.debug("Adding process to runstack of model {}: {}".format(self.name, name))
        self.runstack.append(Process(name, func, *args))
        

    # Adds a process that automatically fills arguments.
    #   e.g. model.addProcessAuto("extractDirectionFromDfsu")
    def addProcessAuto(self, name):

        # Map of auto process name to function and arguments
        PROCESSES = {
                        "extractDirectionFromDfsu" : 
                            [proc.extractDirectionFromDfsu, 
                                self.params["DFSU_REULTS_ANIMATED"], 
                                self.params["DFSU_RESULTS_DIRECTION"], 
                                self.params["DIRECTION_TIMESTEP"]],

                        "createGDB" : 
                            [proc.createGDB,
                                self.params["MODEL_GDB_PATH"],
                                self.name], 

                        "processASC_2DDepth" : 
                            [proc.ascToGDB, 
                                self.params["DEPTH_2D_ASC"], 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["2D_DEPTH_GDB_NAME"]],    

                        "processTIF_2DDepth" : 
                            [proc.dfsuToTif, 
                                self.params["DFSU_RESULTS_MAX"], 
                                "Maximum water depth", 
                                0, # what is this zero for?
                                self.params["2D_DEPTH_TIF_NAME"]],

                        "processASC_2DVelocity" : 
                            [proc.ascToGDB, 
                                self.params["VELOCITY_2D_ASC"], 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["2D_VELOCITY_GDB_NAME"]],   

                        "processASC_2DDirection" : 
                            [proc.ascToGDB, 
                                self.params["DIRECTION_2D_ASC"], 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["2D_DIRECTION_GDB_NAME"]],   

                        "processASC_RiverDepth" : 
                            [proc.ascToGDB, 
                                self.params["DEPTH_RIVER_ASC"], 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["RIVER_DEPTH_GDB_NAME"]],  

                        "processClipResults" : 
                            [proc.clipAllRasters, 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["MODEL_BOUNDARY_POLYGON"],
                                self.params["CLIP_FIELD"], 
                                self.params["CLIP_VALUE"]],  

                        "processCRS" : 
                            [proc.setCRS, 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["CRS"]],  

                        "processMergeRiver2DDepth" : 
                            [proc.mergeRasters, 
                                self.params["2D_DEPTH_GDB_NAME"], 
                                self.params["RIVER_DEPTH_GDB_NAME"], 
                                self.params["FULL_DEPTH_GDB_NAME"], 
                                self.params["MODEL_GDB_PATH"]],

                        "processcleanRasters" : 
                            [proc.cleanRasters, 
                                self.params["MODEL_GDB_PATH"], 
                                self.params["FULL_DEPTH_GDB_NAME"],
                                self.params["2D_VELOCITY_GDB_NAME"],
                                self.params["2D_DIRECTION_GDB_NAME"],
                                self.params["FINAL_DEPTH_GDB_NAME"],
                                self.params["FINAL_VELOCITY_GDB_NAME"],
                                self.params["FINAL_DIRECTION_GDB_NAME"]],

                        "OP_FOR_TESTING_ONLY" : 
                            [proc.FOR_TESTING_ONLY, 
                                self.params["DEPTH_2D_ASC"], 
                                self.params["MODEL_BOUNDARY_POLYGON"]]
                    }

        logging.debug("Adding process to runstack of model {}: {}".format(self.name, name))
        self.runstack.append(Process(name, PROCESSES[name][0], *PROCESSES[name][1:]))  

class Process:
    """
    A class for holding information related to a single function to be run.

    Usage example:
    my_process = Process("process_name", function, *args)
    """

    def __init__(self, name, func, *args):
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        logging.info("Running {}...".format(self.name))
        return self.func(*self.args)
