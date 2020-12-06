import configparser
import logging
from .constants import *
import collections

logging.basicConfig(filename='bb.log', level=logging.DEBUG)

class Hut:
    """
    Main class for setting up single/batch post processing

    Usage example:
    process_manager = Hut("config.ini")
    """
    def __init__(self, config_file = None):
      
        self.config_file = config_file
        self.models = []

        if self.config_file != None:
            self.loadConfig(self.config_file)

    # Allows returning model object by indexing the hut by with model name
    #   e.g. model = myhut["modelname"]
    #   (same as doing myhut.models["modelname"])
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


    def loadConfig(self, config_file):
        """
        Loads a configuration .ini file into the hut.
        """
        logging.info("Loading config file...")

        # Delete any old models
        if not self.models == []:
            logging.info("Removed previous models in hut while loading config file.")
            self.models = []

        # Read the config file
        logging.info("Reading config file.")
        config = configparser.RawConfigParser()
        config.optionxform=str
        config.read(self.config_file)

        # Create empty Model objects for each model
        logging.info("Adding models to hut...")
        models = config.sections()[1:]
        for name in models:
            new_model = Model(name)
            self.models.append(new_model)
            logging.info("Added {} to hut.".format(new_model.name))

        # Import filenames / operations
        logging.info("Importing files and operations into hut models...")
        for model in self.models:
            attributes = config.items(model.name)
            for a in attributes:
                if a[0] in RESULT_FILE_TYPES:
                    model.addFile(*a)
                elif a[0] in PROCESSING_FILE_TYPES:
                    model.addFile(*a)
                elif a[0] in OPERATIONS and a[1] == "True":
                    model.addOperation(a[0])
        
        logging.info("Config file loaded.")


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

    Note: Model instances are intended to be initialized through the Hut object
    """
    def __init__(self, model_name):

        self.name = model_name
        self.results = {}
        self.pfiles = {}
        self.runstack = []

        logging.info("Created model for {}.".format(self.name))

    def addFile(self, file_type, file_path):

        if (file_type in RESULT_FILE_TYPES):
            self.results[file_type] = file_path
            logging.info("Added result file: ".format(file_type))
        elif (file_type in PROCESSING_FILE_TYPES):
            self.pfiles[file_type] = file_path
            logging.info("Added processing file: ".format(file_type))
        else:
            logging.error("{} not a valid file type. Check constants.py for valid types.".format(file_type))

    # NOTE: Need to add a way for operations to accept arguments
    def addOperation(self, operation, *args):

        if (operation in OPERATIONS):
            self.runstack.append([operation, args])
            logging.info("Added operation to runstack: ".format(operation))
        else:
            logging.error("{} not a valid operation type. Check constants.py for valid types.".format(operation))