import busybeaver as bb
import configparser
from busybeaver.constants import *
import os

FILE_DIR = os.path.dirname(__file__)
config_file = os.path.join(FILE_DIR, r"data\test_config.ini")

# ---------------------------------------------------------------------------------------------------------------
# Hut class tests
# ---------------------------------------------------------------------------------------------------------------

# Tests initializing models
# -----
def test_Hut_initialize_models():
    errors = []
    testhut = bb.Hut(config_file)

    if testhut.models[0].name != "newModel1":
        errors.append("Error adding newModel1")
    if testhut.models[1].name != "newModel2":
        errors.append("Error adding newModel2")

    assert not errors, "{}".format("\n".join(errors))

# Tests Hut class magic functions
# -----

def test_Hut_get_model_by_index():

    testhut = bb.Hut(config_file)
    assert testhut["newModel1"].name == "newModel1"

def test_Hut_get_model_by_index2():

    testhut = bb.Hut(config_file)
    assert testhut.models[1].name == "newModel2"

def test_Hut_length_magic():
    testhut = bb.Hut(config_file)
    assert len(testhut) == len(testhut.models)

def test_Hut_model_iteration():
    testhut = bb.Hut(config_file)
    result = 0
    for model in testhut:
        result += 1
    assert result == len(testhut)

def test_Hut_model_iteration2():
    errors = []
    testhut = bb.Hut(config_file)
    index = 0
    for model in testhut:
        if not (model.name == testhut.models[index].name):
            errors.append("Error in iteration.")
        index += 1

    assert not errors, "{}".format("\n".join(errors))

# Tests config file parsing
# -----
def test_Config_parsing1():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    assert models[0] == "newModel1"

def test_Config_parsing2():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    assert models[1] == "newModel2"

def test_Config_parsing3():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    attributes = config.items(models[0])
    assert attributes[0][0] == "includeInProcessing"

def test_Config_parsing3():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    attributes = config.items(models[0])
    assert attributes[0][1] == "True"

def test_Config_parsing4():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    attributes = config.items(models[0])
    assert attributes[9][0] in OPERATIONS

# Tests loading config file attributes
# -----

def test_Hut_load_config_setup1():
    testhut = bb.Hut(config_file)
    assert testhut.output_folder == "PATH"

def test_Hut_load_config_setup2():
    testhut = bb.Hut(config_file)
    assert testhut.crs == "CRS"

def test_Hut_load_config_operations1():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    op_names = []
    for operation in model.runstack:
        op_names.append(operation[0])

    assert "process2DDepth" in op_names    

def test_Hut_load_config_operations2():
    errors = []
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    op_names = []
    for operation in model.runstack:
        op_names.append(operation[0])

    if not "process2DDepth" in op_names:
        errors.append("Error adding process2DDepth operation.")
    if not "process2DDirection" in op_names:
        errors.append("Error adding process2DDirection operation.")
    if not "processFullDepth" in op_names:
        errors.append("Error adding processFullDepth operation.")
    if not "processClipVelocity" in op_names:
        errors.append("Error adding processClean operation.")

    assert not errors, "{}".format("\n".join(errors))

def test_Hut_load_config_operations3():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    op_names = []
    for operation in model.runstack:
        op_names.append(operation[0])

    assert "process2DVelocity" not in op_names

def test_Hut_load_config_result_files1():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    res_names = []
    for result in model.results:
        res_names.append(result)

    assert "DEPTH_2D_ASC" in res_names

def test_Hut_load_config_result_files2():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    res_names = []
    for result in model.results:
        res_names.append(result)

    assert "MODEL_BOUNDARY_POLYGON" not in res_names

def test_Hut_load_config_process_files1():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    res_names = []
    for result in model.pfiles:
        res_names.append(result)

    assert "MODEL_BOUNDARY_POLYGON" in res_names

def test_Hut_load_config_process_files2():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    res_names = []
    for result in model.pfiles:
        res_names.append(result)

    assert "DEPTH_2D_ASC" not in res_names 

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
def test_Model_add_operation_to_run_stack1():

    testhut = bb.Hut(config_file)
    operation = "process2DDepth"
    filename = "somefile.txt"
    testhut["newModel1"].addOperation(operation, filename)

    assert OPERATIONS[testhut["newModel1"].runstack[0][0]] == OPERATIONS["process2DDepth"]

def test_Model_add_operation_to_run_stack2():

    testhut = bb.Hut(config_file)
    operation = "process2DDepth"
    filename = "somefile.txt"
    another_param = "testing *args"
    testhut["newModel1"].addOperation(operation, filename, another_param)

    assert OPERATIONS[testhut["newModel1"].runstack[0][0]] == OPERATIONS["process2DDepth"]

def test_Model_add_operation_to_run_stack3():

    testhut = bb.Hut(config_file)
    operation = "process2DDepth"
    testhut["newModel1"].addOperation(operation)

    assert OPERATIONS[testhut["newModel1"].runstack[0][0]] == OPERATIONS["process2DDepth"]

def test_Model_add_operation_to_run_stack4():

    testhut = bb.Hut(config_file)
    operation = "process2DDepth"
    filename = "somefile.txt"
    another_param = "testing *args"
    testhut["newModel1"].addOperation(operation, filename, another_param)
    id = len(testhut["newModel1"].runstack)

    assert testhut["newModel1"].runstack[id-1][1] == ("somefile.txt", "testing *args")