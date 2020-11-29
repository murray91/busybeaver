import configparser
import logging

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

    def loadConfig(self, config_file):
        """
        Loads a configuration .ini file into the hut.
        """

        logging.info("Reading config file.")
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.models = config.sections()[1:]
        logging.info("Loaded following models: {}".format(self.models))