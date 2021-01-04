import numpy as np 
from mikeio import Dfsu
from mikeio.eum import ItemInfo, EUMType, EUMUnit
from mikeio import Dataset
import gdal
from osgeo import ogr
import os
import logging

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
#   -Current direction unit is radians, but outputs to degrees
#  
def extractDirectionFromDfsu(input_dfsu, output_dfsu, timestep):

    # Make sure timestep is an integer and not string
    timestep = int(timestep)

    # Open dfsu and read specified timestep, then convert rads to degs
    dfs = Dfsu(input_dfsu)
    ds = dfs.read(time_steps=timestep)
    direction = np.rad2deg(ds["Current direction"])

    # Create new dataset for the specified timestep
    items = [ItemInfo("Current direction", EUMType.Current_Direction, EUMUnit.degree)]
    newds = Dataset([direction], ds.time, items)

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
        logging.info("Clipping raster {}...".format(ras))
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
        logging.info("Defining coordinate system for raster {}...".format(ras))
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

    logging.info("Merging rasters {} and {}...".format(raster1, raster2))
    arcpy.MosaicToNewRaster_management("{};{}".format(raster2, raster1), gdb_name, merged_name,
                                   "", "32_BIT_FLOAT", "1", "1",
                                   "LAST", "LAST")

    return True

# cleanRasters
# Renames latest rasters to their final name and removes all others rasters from GDB
#
# Example usage:
#   cleanRasters("gdb_with_rasters.gdb")
# 
def cleanRasters(gdb_name, depth, velocity, direction, depth_final, velocity_final, direction_final):

    import arcpy
    # convert relative paths to absolute to work with arcpy function
    gdb_name = os.path.abspath(gdb_name)
    arcpy.env.workspace = gdb_name

    # check if clipped rasters exist, and if so, use that as final raster
    if arcpy.Exists("{}_CLIPPED".format(depth)):
        depth = "{}_CLIPPED".format(depth)
    if arcpy.Exists("{}_CLIPPED".format(velocity)):
        velocity = "{}_CLIPPED".format(velocity)
    if arcpy.Exists("{}_CLIPPED".format(direction)):
        direction = "{}_CLIPPED".format(direction)

    # Rename rasters to their final names
    logging.info("Renaming final depth, velocity, and direction rasters.")
    arcpy.Rename_management(depth, depth_final)
    arcpy.Rename_management(velocity, velocity_final)
    arcpy.Rename_management(direction, direction_final)

    # Delete all other rasters
    logging.info("Deleting all rasters which are not final.")
    for ras in arcpy.ListRasters("*", "All"):
        if ras != depth_final and ras != velocity_final and ras != direction_final:
            logging.info("Deleting raster {}...".format(ras))
            arcpy.Delete_management(ras)

    return True

# dfsuToTif
# Converts an dfsu file to a tif raster. Overwrites if already exists.        
#
# Example usage:
#   dfsuToTiff("mydfs.dfsu" ,"Total water depth", 30, "mytif.tif")
# 
def dfsuToTif(dfsu_file, item, time_step, tif_file):

    # get absolute paths to files
    dfsu_file = os.path.abspath(dfsu_file)
    tif_file = os.path.abspath(tif_file)

    # open dfsu, get points, then close to save memory
    dfs = Dfsu(dfsu_file)
    coords = dfs.element_coordinates[:,:2]

    # get custom nx ny based on what MIKE Zero gives
    x0 = np.min(coords, axis = 0)[0]
    y0 = np.min(coords, axis = 0)[1]
    x1 = np.max(coords, axis = 0)[0]
    y1 = np.max(coords, axis = 0)[1]
    nx = round((x1-x0)/19*20)
    ny = round((y1-y0)/19*20)
    grid = dfs.get_overset_grid(shape=(nx, ny))
    
    ds = dfs.read(item, time_step)
    data = ds.data[0].transpose()
    points = np.append(coords, data, axis=1)
    dfs = None
    ds = None

    # write points to temporary shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.CreateDataSource('temp_points.shp')
    layer = ds.CreateLayer("points", srs=None, geom_type=ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("Elevation", ogr.OFTReal))
    for point in points:
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("Elevation", point[2])
        pnt = ogr.Geometry(ogr.wkbPoint)
        pnt.AddPoint(point[0], point[1])
        feature.SetGeometry(pnt)
        layer.CreateFeature(feature)
        feature = None
    ds = None

    # delete any old tif files
    try:
        os.remove(tif_file)
    except OSError:
        pass

    # interpolate points to grid and write to shapefile
    option = gdal.GridOptions(
        format='GTiff', 
        outputType=gdal.gdalconst.GDT_Float32,
        outputBounds=[grid.x0, grid.y1, grid.x1, grid.y0], 
        width=grid.nx, 
        height=grid.ny,
        #algorithm='invdist:power=2.0:smoothing=0.5:radius1=25.0:radius2=25.0:angle=0.0:max_points=0:min_points=0:nodata=-9999',
        algorithm='invdistnn:power=2.0:smoothing=0:radius=25.0:max_points=0:min_points=0:nodata=-9999',
        #algorithm='average:radius1=1:radius2=1',
        zfield='Elevation',
        noData=-9999)
    out = gdal.Grid(tif_file, 'temp_points.shp', options=option) 
    out = None

    # clean up temporary shapefile
    #driver.DeleteDataSource('temp_points.shp')

    logging.info("Created raster: {}".format(tif_file))

    return True