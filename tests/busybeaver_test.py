import busybeaver as bb
import busybeaver.processes as proc
import configparser
import os

# ---------------------------------------------------------------------------------------------------------------
# Hut class tests
# ---------------------------------------------------------------------------------------------------------------

# Tests Hut class magic functions
# -----

def makeHutWithModels():
    testhut = bb.Hut()
    testhut.models.append(bb.Model("newModel1"))
    testhut.models.append(bb.Model("newModel2"))

    testhut['newModel1'].params["DEPTH_2D_ASC"] = "Some path to asc file."
    testhut['newModel1'].params["MODEL_GDB_PATH"] = "Path to gdb"

    return testhut

def test_Hut_get_model_by_index():

    testhut = makeHutWithModels()
    assert testhut["newModel1"].name == "newModel1"

def test_Hut_get_model_by_index2():

    testhut = makeHutWithModels()
    assert testhut.models[1].name == "newModel2"

def test_Hut_length_magic():
    testhut = makeHutWithModels()
    assert len(testhut) == len(testhut.models)

def test_Hut_model_iteration():
    testhut = makeHutWithModels()
    result = 0
    for model in testhut:
        result += 1
    assert result == len(testhut)

def test_Hut_model_iteration2():
    errors = []
    testhut = makeHutWithModels()
    index = 0
    for model in testhut:
        if not (model.name == testhut.models[index].name):
            errors.append("Error in iteration.")
        index += 1

    assert not errors, "{}".format("\n".join(errors))

# Tests for adding a process automatically to the model run stack
# -----
def test_Model_add_process_to_run_stack1():

    testhut = makeHutWithModels()
    testhut["newModel1"].addProcessAuto("processASC_2DDepth")

    assert testhut["newModel1"].runstack[0].name == "processASC_2DDepth"

def test_Model_add_process_to_run_stack2():

    testhut = makeHutWithModels()
    testhut["newModel1"].addProcessAuto("processASC_2DDepth")

    assert testhut["newModel1"].runstack[0].func == proc.ascToGDB

def test_Model_add_process_to_run_stack4():

    errors = []
    testhut = makeHutWithModels()
    testhut["newModel1"].addProcessAuto("processASC_2DDepth")
    testhut["newModel1"].addProcessAuto("createGDB")
    testhut["newModel1"].addProcessAuto("processMergeRiver2DDepth")
    model = testhut["newModel1"]
    for i in model.runstack:
        if not callable(i.func):
            errors.append("Runstack function not callable.")

    assert not errors, "{}".format("\n".join(errors))

def test_Model_add_process_to_run_stack5():

    testhut = makeHutWithModels()
    testhut["newModel1"].addProcessAuto("processASC_2DDepth")
    model = testhut["newModel1"]
    assert model.runstack[0].args[0] == "Some path to asc file."

def test_Model_add_process_to_run_stack6():

    testhut = makeHutWithModels()
    testhut["newModel1"].addProcessAuto("processASC_2DDepth")
    model = testhut["newModel1"]
    assert model.runstack[0].args[1] == "Path to gdb"

def test_Model_add_custom_process1():

    testhut = makeHutWithModels()
    model = testhut["newModel1"]

    def myfunct(*args):
        return args[0]

    myargs = "it works!"
    my_cust_opx = myfunct
    model.addProcess("my process", my_cust_opx, myargs)
    assert model.runstack[len(model.runstack)-1].run() == "it works!"

# ---------------------------------------------------------------------------------------------------------------
# Process class tests
# ---------------------------------------------------------------------------------------------------------------

name = "my function"
def adding(x, y):
    return x + y
args = 2, 2

def test_process_add_function1():  
    myProcess = bb.Process(name, adding, *args)
    assert myProcess.name == "my function"

def test_process_add_function2():  
    myProcess = bb.Process(name, adding, *args)
    assert myProcess.func == adding

def test_process_add_function3():  
    myProcess = bb.Process(name, adding, *args)
    assert args == myProcess.args

def test_process_add_function4():  
    myProcess = bb.Process(name, adding, *args)
    assert myProcess.run() == 4

def test_process_add_function5():  
    myProcess = bb.Process(name, adding, 20, 15)
    assert myProcess.run() == 35