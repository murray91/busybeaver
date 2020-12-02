import busybeaver as bb
from busybeaver.constants import *
import os

FILE_DIR = os.path.dirname(__file__)
config_file = os.path.join(FILE_DIR, r"data\test_config.ini")

# ---------------------------------------------------------------------------------------------------------------
# Hut class tests
# ---------------------------------------------------------------------------------------------------------------

# Test hut initialization of models from config file
def test_Hut_initialize_models():
    errors = []
    testhut = bb.Hut(config_file)

    if testhut.models["newModel1"].name != "newModel1":
        errors.append("Error adding newModel1")
    if testhut.models["newModel2"].name != "newModel2":
        errors.append("Error adding newModel2")

    assert not errors, "{}".format("\n".join(errors))

def test_Hut_get_model_by_index():

    testhut = bb.Hut(config_file)

    assert testhut["newModel1"].name == "newModel1"

# ---------------------------------------------------------------------------------------------------------------
# Model class tests
# ---------------------------------------------------------------------------------------------------------------

# Tests for adding a result file to a model
# -----
def test_Model_add_result_1():
    file_type = "DEPTH_2D_ASC"
    fake_path = r"C:\Some\Fake\Path\afile.asc"
    model = bb.Model("TestModel")
    model.addFile(file_type, fake_path)

    assert file_type in model.results and not model.pfiles, "Trouble adding result file to Model object."

def test_Model_add_result_2():
    file_type = "WRONG_FILE_TYPE"
    fake_path = r"C:\Some\Fake\Path\afile.asc"
    model = bb.Model("TestModel")
    model.addFile(file_type, fake_path)

    assert not model.results and not model.pfiles, "Trouble adding result file to Model object."

# Tests for adding a processing file to a model
# -----
def test_Model_add_processing_1():
    file_type = "MODEL_BOUNDARY_POLYGON"
    fake_path = r"C:\Some\Fake\Path\afile.shp"
    model = bb.Model("TestModel")
    model.addFile(file_type, fake_path)

    assert file_type in model.pfiles and not model.results, "Trouble adding processing file to Model object."

def test_Model_add_processing_2():
    file_type = "WRONG_FILE_TYPE"
    fake_path = r"C:\Some\Fake\Path\afile.shp"
    model = bb.Model("TestModel")
    model.addFile(file_type, fake_path)

    assert not model.results and not model.pfiles, "Trouble adding processing file to Model object."

# Tests for adding an operation to the model run stack
# -----
def test_Model_add_operation_to_run_stack():

    testhut = bb.Hut(config_file)
    operation = "ASC_TO_RASTER"
    testhut["newModel1"].addOpx(operation)

    assert testhut["newModel1"].runstack[0] == OPERATIONS["ASC_TO_RASTER"]