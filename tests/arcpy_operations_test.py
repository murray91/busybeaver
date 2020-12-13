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
import arcpy

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
        "DEPTH_RIVER_ASC" : None,
        "VELOCITY_2D_ASC" : r"tests\data\MIKE\test_max_results_speed0.asc",
        "DIRECTION_2D_ASC" : r"tests\data\MIKE\test_animated_results_direction32.asc",
    }

    process_files = {
        "MODEL_BOUNDARY_POLYGON" : None,
        "DEPTH_RIVER_MASK_POLYGON" : None, 
        "DFSU_RESULTS_DIRECTION" : r"tests\data\test_output\test_animed_results_direction.dfsu",
    }

    params = {
        "MODEL_NAME" : "testmodel",
        "MODEL_GDB_PATH" : r"tests\data\test_output\testmodel.gdb",
        "DIRECTION_TIMESTEP" : 32,     
    }

    model = hut["testmodel"]
    model.results.update(result_files)
    model.pfiles.update(process_files)
    model.params.update(params)
    model.addPredefinedOperation("extractDirectionFromDfsu")
    hut.output_folder = r"tests\data\test_output"
    hut.saveConfig(r"tests\data\test_output\testhut.ini")

    return hut

# ---------------------------------------------------------------------------------------------------------------
#File assertion tests
# ---------------------------------------------------------------------------------------------------------------

@pytest.mark.arcpy
def test_compare_two_files1():
    hut = testHut()
    model = hut["testmodel"]
    file1 = model.results["DFSU_RESULTS_MAX"]
    file2 = model.results["DFSU_RESULTS_MAX"]
    assert filecmp.cmp(file1, file2)

@pytest.mark.arcpy
def test_compare_two_files2():
    hut = testHut()
    model = hut["testmodel"]
    file1 = model.results["DFSU_RESULTS_MAX"]
    file2 = model.results["DIRECTION_2D_ASC"]
    assert not filecmp.cmp(file1, file2)

# ---------------------------------------------------------------------------------------------------------------
# Extract direction at specific timestep
# ---------------------------------------------------------------------------------------------------------------
@pytest.mark.arcpy
def test_Operation_extract_direction1():
    hut = testHut()
    model = hut["testmodel"]
    opx.extractDirectionFromDfsu(model.results["DFSU_REULTS_ANIMATED"], model.pfiles["DFSU_RESULTS_DIRECTION"], 32)

    # check if dfsu data shape and values are same
    data1 = Dfsu(model.results["DFSU_REULTS_ANIMATED"]).read(time_steps=32)["Current direction"]
    data2 = Dfsu(model.pfiles["DFSU_RESULTS_DIRECTION"]).read(time_steps=0)["Current direction"]
    assert np.allclose(data1, data2,1e-05,equal_nan=True)

@pytest.mark.arcpy
def test_Operation_extract_direction2():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("extractDirectionFromDfsu")
    model.runstack[len(model.runstack)-1].run()

    data1 = Dfsu(model.results["DFSU_REULTS_ANIMATED"]).read(time_steps=32)["Current direction"]
    data2 = Dfsu(model.pfiles["DFSU_RESULTS_DIRECTION"]).read(time_steps=0)["Current direction"]
    assert np.allclose(data1, data2,1e-05,equal_nan=True)

# ---------------------------------------------------------------------------------------------------------------
# Create geodatabase for model results, if not existing already
# ---------------------------------------------------------------------------------------------------------------

def test_Operation_create_gdb_args1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("createGDB")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.func == opx.createGDB

def test_Operation_create_gdb_args2():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("createGDB")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args == (r"tests\data\test_output\testmodel.gdb", "testmodel")

@pytest.mark.arcpy
def test_Operation_create_gdb1():
    hut = testHut()
    model = hut["testmodel"]

    if os.path.exists(model.params["MODEL_GDB_PATH"]):
        shutil.rmtree(model.params["MODEL_GDB_PATH"])

    model.addPredefinedOperation("createGDB")
    model.runstack[len(model.runstack)-1].run()

    assert os.path.exists(model.params["MODEL_GDB_PATH"])

# ---------------------------------------------------------------------------------------------------------------
# Converts ASC depth files to gdb
# ---------------------------------------------------------------------------------------------------------------

def test_Operation_processASC_2DDepth_args1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDepth")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.func == opx.ascToGDB

def test_Operation_processASC_2DDepth_args2():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDepth")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[0] == r"tests\data\MIKE\test_max_results_depth0.asc"

def test_Operation_processASC_2DDepth_args3():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDepth")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[1] == r"tests\data\test_output\testmodel.gdb"

def test_Operation_processASC_2DDepth_args4():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDepth")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[2] == "testmodel_2D_Depth"

@pytest.mark.arcpy
def test_Operation_processASC_2DDepth_1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDepth")
    rs = model.runstack[len(model.runstack)-1]
    rs.run()

    arcpy.env.workspace = model.params["MODEL_GDB_PATH"]
    rasterExists = arcpy.Exists(rs.args[2])

    assert rasterExists

# ---------------------------------------------------------------------------------------------------------------
# Converts ASC velocity files to gdb
# ---------------------------------------------------------------------------------------------------------------

def test_Operation_processASC_2DVelocity_args1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DVelocity")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.func == opx.ascToGDB

def test_Operation_processASC_2DVelocity_args2():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DVelocity")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[0] == r"tests\data\MIKE\test_max_results_speed0.asc"

def test_Operation_processASC_2DVelocity_args3():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DVelocity")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[1] == r"tests\data\test_output\testmodel.gdb"

def test_Operation_processASC_2DVelocity_args4():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DVelocity")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[2] == "testmodel_2D_Velocity"

@pytest.mark.arcpy
def test_Operation_processASC_2DVelocity_1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DVelocity")
    rs = model.runstack[len(model.runstack)-1]
    rs.run()

    arcpy.env.workspace = model.params["MODEL_GDB_PATH"]
    rasterExists = arcpy.Exists(rs.args[2])

    assert rasterExists

# ---------------------------------------------------------------------------------------------------------------
# Converts ASC direction files to gdb
# ---------------------------------------------------------------------------------------------------------------

def test_Operation_processASC_2DDirection_args1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDirection")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.func == opx.ascToGDB

def test_Operation_processASC_2DDirection_args2():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDirection")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[0] == r"tests\data\MIKE\test_animated_results_direction32.asc"

def test_Operation_processASC_2DDirection_args3():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDirection")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[1] == r"tests\data\test_output\testmodel.gdb"

def test_Operation_processASC_2DDirection_args4():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDirection")
    rs = model.runstack[len(model.runstack)-1]
    assert rs.args[2] == "testmodel_2D_Direction"

@pytest.mark.arcpy
def test_Operation_processASC_2DDirection_1():
    hut = testHut()
    model = hut["testmodel"]
    model.addPredefinedOperation("processASC_2DDirection")
    rs = model.runstack[len(model.runstack)-1]
    rs.run()

    arcpy.env.workspace = model.params["MODEL_GDB_PATH"]
    rasterExists = arcpy.Exists(rs.args[2])

    assert rasterExists