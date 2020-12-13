import numpy as np 
from mikeio import Dfsu
from mikeio.eum import ItemInfo, EUMType, EUMUnit
from mikeio import Dataset
import os
import logging
import arcpy

logging.basicConfig(filename='bb.log', level=logging.DEBUG)

def TEMPORARY(*args):
    return "TEST"

# Returns the values of constants passed to it
def FOR_TESTING_ONLY(*args):
    return [*args]

# extractDirectionFromDfsu
# Saves direction from specified timestep to a new dfsu
# Useful for dealing with large dfsu files
#
# Example usage:
#   extractDirectionFromDfsu("mydfsu.dfsu", "mydfsu_direction", 30)  
# 
# Assumes
#   -input dfsu has Current direction
#   -timestep specified exists
#   -Current direction unit is radians
#  
def extractDirectionFromDfsu(input_dfsu, output_dfsu, timestep):

    # Make sure timestep is an integer and not string
    timestep = int(timestep)

    # Open dfsu and read specified timestep
    dfs = Dfsu(input_dfsu)
    ds = dfs.read(time_steps=timestep)

    # Create new dataset for the specified timestep
    items = [ItemInfo("Current direction", EUMType.Current_Direction, EUMUnit.radian)]
    newds = Dataset([ds["Current direction"]], ds.time, items)

    # Write direction to new dfsu
    dfs.write(output_dfsu, newds)
    
    return True

# createGDB
# Creates a geodatabase for model
#
# Example usage:
#   createGD("C:/some/path/to", "Name of GDB")
# 

def createGDB(gdb_path, gdb_name):

    if not os.path.exists(gdb_path):
        logging.info("Geobatase doesn't exist for {}. Creating now.".format(gdb_name))
        arcpy.env.workspace = os.getcwd()
        arcpy.CreateFileGDB_management(os.path.dirname(gdb_path), gdb_name)
        logging.info("Geodatabase created at:\n{}".format(gdb_path))
    else:
        logging.info("Geodatabase already exists for {}.".format(gdb_name))
    
    return True

# ascToGDB
# Converts an asc file to a raster and adds it to gdb. Overwrites if already exists.        
#
# Example usage:
#   ascToGDB("myascfile.asc", "somegdb.gdb")
# 
def ascToGDB(asc_file, gdb_name, raster_name = None):

    # convert relative paths to absolute to work with arcpy function
    asc_file = os.path.abspath(asc_file)
    arcpy.env.workspace = gdb_name

    # use same raster name as asc file if not specified
    if raster_name == None:
        gdb_raster_name = os.path.splitext(os.path.basename(asc_file))[0]

    arcpy.ASCIIToRaster_conversion(asc_file, raster_name, data_type="FLOAT")

    logging.info("Created raster: {}".format(raster_name))

# processFullDepth
# Insert description of function
# Example usage: ...
def processFullDepth(*args):
    return None

# processClipDepth
# Insert description of function
# Example usage: ...
def processClipDepth(*args):
    return None

# processClipVelocity
# Insert description of function
# Example usage: ...
def processClipVelocity(*args):
    return None

# processClean
# Insert description of function
# Example usage: ...
def processClean(*args):
    return None