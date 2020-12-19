import busybeaver as bb
import configparser
from busybeaver.constants import *
import os
import shutil
import pytest
import filecmp
import busybeaver.operations as opx
from mikeio import Dfsu
import numpy as np
import gdal
import math

# These tests require an arcpy license to run and can take long to run

# ---------------------------------------------------------------------------------------------------------------
# Setup hut for testing arcpy tests
# ---------------------------------------------------------------------------------------------------------------

def testHut():
    hut = bb.Hut()
    hut.models.append(bb.Model("testmodel"))

    result_files = {
        "DFSU_REULTS_ANIMATED" : r"tests\data\MIKE\test_animated_results.dfsu",
        "DFSU_RESULTS_MAX" : r"tests\data\MIKE\test_max_results.dfsu",     
        "DEPTH_2D_ASC" : r"tests\data\MIKE\test_max_results_depth0.asc",
        "2D_DEPTH_TIF_NAME" : r"tests\data\test_output\max_depth.tif",
        "DEPTH_RIVER_ASC" : r"tests\data\MIKE\test_max_results_depth0.asc",
        "VELOCITY_2D_ASC" : r"tests\data\MIKE\test_max_results_speed0.asc",
        "DIRECTION_2D_ASC" : r"tests\data\MIKE\test_animated_results_direction32.asc",
    }

    process_files = {
        "MODEL_BOUNDARY_POLYGON" : r"tests\data\clip_polygons.shp",
        "DEPTH_RIVER_MASK_POLYGON" : None, 
        "DFSU_RESULTS_DIRECTION" : r"tests\data\test_output\test_animed_results_direction.dfsu",
    }

    params = {
        "MODEL_NAME" : "testmodel",
        "MODEL_GDB_PATH" : r"tests\data\test_output\testmodel.gdb",
        "DIRECTION_TIMESTEP" : 32,     
        "CLIP_FIELD" : "Name",
        "CLIP_VALUE" : "testmodel",
        "CRS" : "ETRS 1989 UTM Zone 32N",
    }

    model = hut["testmodel"]
    model.results.update(result_files)
    model.pfiles.update(process_files)
    model.params.update(params)
    hut.output_folder = r"tests\data\test_output"
    hut.saveConfig(r"tests\data\test_output\testhut.ini")

    return hut

# tolerance for difference between mike interpolation and gdal
tolerance = 0.05

@pytest.mark.gdal
def test_dfsuToTif_1():
    # test if it creates a tif file
    hut = testHut()
    model = hut["testmodel"]

    # remove any tif files from old tests
    try:
        os.remove(model.results["2D_DEPTH_TIF_NAME"])
    except OSError:
        pass

    model.addPredefinedOperation("processTIF_2DDepth")
    model.runstack[len(model.runstack)-1].run()

    assert os.path.exists(model.results["2D_DEPTH_TIF_NAME"])

@pytest.mark.gdal
def test_dfsuToTif_2():
    # test if temp shapefile is deleted
    hut = testHut()
    model = hut["testmodel"] 

    assert not os.path.exists("temp_points.shp")

@pytest.mark.gdal
def test_dfsuToTif_depth_comp_asc_3():
    # test if it provides similar results to asc from MIKE
    hut = testHut()
    model = hut["testmodel"] 

    ds_asc = gdal.Open(r"tests\data\MIKE\test_max_results_depth0.asc")
    arr_asc = np.array(ds_asc.ReadAsArray())
    ds_asc = None

    ds_tif = gdal.Open(model.results["2D_DEPTH_TIF_NAME"])
    arr_tif = np.array(ds_tif.ReadAsArray())
    ds_tif = None

    assert math.isclose(np.max(arr_asc), np.max(arr_tif), abs_tol=tolerance)

@pytest.mark.gdal
def test_dfsuToTif_depth_comp_asc_4():
    # test if it provides similar results to asc from MIKE
    hut = testHut()
    model = hut["testmodel"] 

    ds_asc = gdal.Open(r"tests\data\MIKE\test_max_results_depth0.asc")
    arr_asc = np.array(ds_asc.ReadAsArray())
    ds_asc = None

    ds_tif = gdal.Open(model.results["2D_DEPTH_TIF_NAME"])
    arr_tif = np.array(ds_tif.ReadAsArray())
    ds_tif = None

    assert math.isclose(np.mean(arr_asc), np.mean(arr_tif), abs_tol=tolerance)

@pytest.mark.gdal
def test_dfsuToTif_depth_comp_asc_5():
    # test if it provides similar results to asc from MIKE
    hut = testHut()
    model = hut["testmodel"] 

    ds_asc = gdal.Open(r"tests\data\MIKE\test_max_results_depth0.asc")
    arr_asc = np.array(ds_asc.ReadAsArray())
    ds_asc = None

    ds_tif = gdal.Open(model.results["2D_DEPTH_TIF_NAME"])
    arr_tif = np.array(ds_tif.ReadAsArray())
    ds_tif = None

    assert math.isclose(arr_asc[3][1], arr_tif[3][1], abs_tol=tolerance)

@pytest.mark.gdal
def test_dfsuToTif_depth_comp_asc_6():
    # test if it provides similar results to asc from MIKE
    hut = testHut()
    model = hut["testmodel"] 

    ds_asc = gdal.Open(r"tests\data\MIKE\test_max_results_depth0.asc")
    arr_asc = np.array(ds_asc.ReadAsArray())
    ds_asc = None

    ds_tif = gdal.Open(model.results["2D_DEPTH_TIF_NAME"])
    arr_tif = np.array(ds_tif.ReadAsArray())
    ds_tif = None

    assert np.allclose(arr_asc, arr_tif,tolerance,equal_nan=True)