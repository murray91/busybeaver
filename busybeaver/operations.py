import numpy as np 
from mikeio import Dfsu
from mikeio.eum import ItemInfo, EUMType, EUMUnit
from mikeio import Dataset
import os
import logging

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

    import arcpy

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

    import arcpy

    # convert relative paths to absolute to work with arcpy function
    asc_file = os.path.abspath(asc_file)
    gdb_name = os.path.abspath(gdb_name)
    arcpy.env.workspace = gdb_name

    # use same raster name as asc file if not specified
    if raster_name == None:
        gdb_raster_name = os.path.splitext(os.path.basename(asc_file))[0]

    arcpy.ASCIIToRaster_conversion(asc_file, raster_name, data_type="FLOAT")

    logging.info("Created raster: {}".format(raster_name))

    return True

# clipAllRasters
# Clips all rasters in gdb to a polygon found in a shapefile matching field name and id
#
# Example usage:
#   clipAllRasters("mygdb.gdb", "some_clip_file.shp", "selection field name", "polygon id")
# 
def clipAllRasters(gdb_name, clip_shapefile, clip_field, field_value):

    import arcpy

    # convert relative paths to absolute to work with arcpy function
    clip_shapefile = os.path.abspath(clip_shapefile)
    gdb_name = os.path.abspath(gdb_name)
    arcpy.env.workspace = gdb_name

    # Get clip geometry for specific model shapefile with several polygons
    f = arcpy.FeatureSet(clip_shapefile)
    cursor = arcpy.da.SearchCursor(f, ("{}".format(clip_field), "SHAPE@"),"""{}='{}'""".format(clip_field, field_value))
    cursor.reset()
    geom = None
    for row in cursor:
        geom = row[1]       

    # Clip rasters
    for ras in arcpy.ListRasters("*", "All"):
        arcpy.Clip_management(
            in_raster = ras, 
            out_raster = "{}_CLIPPED".format(ras),
            in_template_dataset = geom,
            clipping_geometry = "ClippingGeometry")

    return True

# setCRS
# Sets the CRS of all rasters in a gdb
#
# Example usage:
#   setCRS("somegdb.gdb", "ETRS 1989 UTM Zone 32N")
# 
def setCRS(gdb_name, crs):

    import arcpy

    # convert relative paths to absolute to work with arcpy function
    gdb_name = os.path.abspath(gdb_name)
    arcpy.env.workspace = gdb_name

    sr = arcpy.SpatialReference(crs)

    # set coordinate system for all rasters
    for ras in arcpy.ListRasters("*", "All"):
        arcpy.DefineProjection_management(ras, sr)

    return True

# mergeRasters
# Merges two rasters. Raster 1 values take priority of Raster 2.
#
# Example usage:
#   mergeRasters("raster1", "raster2", #merged raster", "gdb_with_both_rasters.gdb")
# 
def mergeRasters(raster1, raster2, merged_name, gdb_name):

    import arcpy

    # convert relative paths to absolute to work with arcpy function
    gdb_name = os.path.abspath(gdb_name)
    arcpy.env.workspace = gdb_name

    arcpy.MosaicToNewRaster_management("{};{}".format(raster2, raster1), gdb_name, merged_name,
                                   "", "32_BIT_FLOAT", "1", "1",
                                   "LAST", "LAST")

    return True

# processClean
# Insert description of function
# Example usage: ...
def processClean(*args):
    return None