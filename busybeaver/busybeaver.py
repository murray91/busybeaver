import configparser
import logging
from .constants import *
import collections
import os

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
        logging.info("Starting to run operations for all models.")
        for model in self.models:
            logging.info("Running operations for {}...".format(model.name))
            for opx in model.runstack:
                opx.run()

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
        
        logging.info("Created model: {}.".format(self.name))
        self.name = model_name
        self.runstack = []
        self.params = {
                "DFSU_REULTS_ANIMATED",     # animated dfsu results from MIKE
                "DFSU_RESULTS_MAX",         # max dfsu results from MIKE
                "DEPTH_2D_ASC",             # MIKE 2d max depth in asc format
                "DEPTH_RIVER_ASC",          # MIKE river max depth in asc format
                "VELOCITY_2D_ASC",          # MIKE 2d max velocity in asc format
                "DIRECTION_2D_ASC"          # MIKE 2d direction in asc format
                "MODEL_BOUNDARY_POLYGON",   # Boundaries to clip model results to
                "DEPTH_RIVER_MASK_POLYGON", # Polygon areas to be removed from DEPTH_RIVER
                "DFSU_RESULTS_DIRECTION",   # Output location for extractDirectionFromDfsu
                "MODEL_NAME",               # Name/alias of the model
                "MODEL_PATH",               # Path to model output folder
                "MODEL_GDB_PATH",           # Path to the model's GDB
                "DIRECTION_TIMESTEP",       # Integer timestep to extract direction from dfsu in model
                "2D_DEPTH_TIF_NAME",        # Name of 2d depth raster (exclusing river) in tif format
                "2D_DEPTH_GDB_NAME",        # Name of 2d depth raster (exclusing river) in gdb
                "2D_VELOCITY_GDB_NAME",     # Name of 2d velocity raster (exclusing river) in gdb ... unclipped
                "2D_DIRECTION_GDB_NAME",    # Name of 2d direction raster (excluding river) in gdb ... unclipped
                "RIVER_DEPTH_GDB_NAME",     # Name of 2d river depth raster in gdb ... unclipped
                "FULL_DEPTH_GDB_NAME",      # Name of full depth raster (2d and river merged) ... unclipped
                "FINAL_DEPTH_GDB_NAME",     # Final name of depth raster after clipping
                "FINAL_VELOCITY_GDB_NAME",  # Final name of velocity raster after clipping
                "FINAL_DIRECTION_GDB_NAME", # Final name of direction raster after clipping
                "CLIP_FIELD",               # Name of column in attribute table of MODEL_BOUNDARY_POLYGON
                "CLIP_VALUE",               # Value in CLIP_FIELD to use as clip olygon
                "CRS",                      # Coordinate system string for all rasters (e.g. 'ETRS 1989 UTM Zone 32N')
        }

    # Adds a raw python function and arguments to runstack
    def addOperation(self, name, func, *args):
        self.runstack.append(Operation(name, func, *args))
        logging.debug("Added operation to runstack of model {}: {}".format(self.name, name))

class Operation:
    """
    A class for holding information related to a single function to be run.

    Usage example:
    my_operation = Operation("operation_name", function, *args)
    """

    def __init__(self, name, func, *args):
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        logging.info("Running {}...".format(self.name))
        return self.func(*self.args)
