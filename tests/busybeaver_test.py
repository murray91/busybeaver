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

def test_Config_parsing4():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    attributes = config.items(models[0])
    assert attributes[0][1] == "True"

def test_Config_parsing5():
    config = configparser.RawConfigParser()
    config.optionxform=str
    config.read(config_file)
    models = config.sections()[1:]
    attributes = config.items(models[0])
    assert attributes[13][0] in OPERATIONS

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
    
    funcs = []
    for operation in model.runstack:
        funcs.append(operation.func)

    assert OPERATIONS["processASC_2DDepth"][0] in funcs

def test_Hut_load_config_operations2():
    errors = []
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    funcs = []
    for operation in model.runstack:
        funcs.append(operation.name)

    if not "processASC_2DDepth" in funcs:
        errors.append("Error adding processASC_2DDepth operation.")
    if not "processASC_2DDirection" in funcs:
        errors.append("Error adding processASC_2DDirection operation.")
    if not "processFullDepth" in funcs:
        errors.append("Error adding processFullDepth operation.")
    if not "processClipVelocity" in funcs:
        errors.append("Error adding processClean operation.")

    assert not errors, "{}".format("\n".join(errors))

def test_Hut_load_config_operations3():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    
    op_names = []
    for operation in model.runstack:
        op_names.append(operation.name)

    assert "processASC_2DVelocity" not in op_names

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

def test_Hut_load_config_params1():
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]

    assert "DIRECTION_TIMESTEP" in model.params

# TODO: WRITE TESTS FOR SAVE CONFIG

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

# Tests for adding a parameter to a model
# -----
def test_Model_add_param_1():
    param = "DIRECTION_TIMESTEP"
    model = bb.Model("TestModel")
    model.addParam(param, 30)

    assert param in model.params, "Trouble adding parameter to Model object."

def test_Model_add_param_2():
    param = "INVALID PARAM"
    model = bb.Model("TestModel")
    model.addParam(param, 30)

    assert param not in model.params, "Trouble adding parameter to Model object."

# Tests for adding an operation to the model run stack
# -----
def test_Model_add_operation_to_run_stack1():

    testhut = bb.Hut(config_file)
    operation = "processASC_2DDepth"
    testhut["newModel1"].addPredefinedOperation(operation)

    assert testhut["newModel1"].runstack[0].name == "processASC_2DDepth"

def test_Model_add_operation_to_run_stack2():

    testhut = bb.Hut(config_file)
    operation = "processASC_2DDepth"
    testhut["newModel1"].addPredefinedOperation(operation)

    assert testhut["newModel1"].runstack[0].func == OPERATIONS["processASC_2DDepth"][0]

def test_Model_add_operation_to_run_stack4():

    errors = []
    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    for i in model.runstack:
        if not callable(i.func):
            errors.append("Runstack function not callable.")

    assert not errors, "{}".format("\n".join(errors))

def test_Model_add_operation_to_run_stack5():

    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    assert model.runstack[0].args[0] == "Some path to asc file."

def test_Model_add_operation_to_run_stack6():

    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    model.addPredefinedOperation("OP_FOR_TESTING_ONLY")
    expected_result = [model.results["DEPTH_2D_ASC"], model.pfiles["MODEL_BOUNDARY_POLYGON"]]
    assert expected_result == model.runstack[len(model.runstack)-1].run()

def test_Model_add_operation_to_run_stack7():

    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    model.addPredefinedOperation("extractDirectionFromDfsu")
    assert model.runstack[len(model.runstack)-1].args[0] == "My dfsu animated results"

def test_Model_add_operation_to_run_stack8():

    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    model.addPredefinedOperation("extractDirectionFromDfsu")
    assert model.runstack[len(model.runstack)-1].args[1] == "Direction path123"

def test_Model_add_operation_to_run_stack9():

    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]
    model.addPredefinedOperation("extractDirectionFromDfsu")
    assert int(model.runstack[len(model.runstack)-1].args[2]) == 32

def test_Model_add_custom_operation1():

    testhut = bb.Hut(config_file)
    model = testhut["newModel1"]

    def myfunct(*args):
        return args[0]

    myargs = "it works!"
    my_cust_opx = myfunct
    model.addOperation(my_cust_opx, myargs)
    assert model.runstack[len(model.runstack)-1].run() == "it works!"

# ---------------------------------------------------------------------------------------------------------------
# Operation class tests
# ---------------------------------------------------------------------------------------------------------------

name = "my function"
def adding(x, y):
    return x + y
args = 2, 2

def test_Operation_add_function1():  
    opx = bb.Operation(name, adding, *args)
    assert opx.name == "my function"

def test_Operation_add_function2():  
    opx = bb.Operation(name, adding, *args)
    assert opx.func == adding

def test_Operation_add_function3():  
    opx = bb.Operation(name, adding, *args)
    assert args == opx.args

def test_Operation_add_function4():  
    opx = bb.Operation(name, adding, *args)
    assert opx.run() == 4

def test_Operation_add_function5():  
    opx = bb.Operation(name, adding, 20, 15)
    assert opx.run() == 35