import busybeaver as bb
import configparser
from busybeaver.constants import *
import os
import pytest

# These tests require an arcpy license to run and can take long to run

# ---------------------------------------------------------------------------------------------------------------
# Setup hut for testing arcpy tests
# ---------------------------------------------------------------------------------------------------------------

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
    "DIRECTION_TIMESTEP" : 32,     
}

hut["testmodel"].results.update(result_files)
hut["testmodel"].pfiles.update(process_files)
hut["testmodel"].params.update(process_files)
hut["testmodel"].params.update(process_files)
hut["testmodel"].addPredefinedOperation("extractDirectionFromDfsu")
hut.output_folder = r"tests\data\test_output"
hut.saveConfig(r"tests\data\test_output\testhut.ini")

# ---------------------------------------------------------------------------------------------------------------
# Extract direction at specific timestep
# ---------------------------------------------------------------------------------------------------------------
@pytest.mark.arcpy
def test_Operation_extract_direction():

    assert 1==1