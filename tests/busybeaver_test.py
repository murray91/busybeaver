import busybeaver as bb
import os

FILE_DIR = os.path.dirname(__file__)
config_file = os.path.join(FILE_DIR, r"data\test_config.ini")

# Hut initialization tests
def test_Hut_initialize_models():
    testhut = bb.Hut(config_file)
    assert testhut.models == ["newModel1", "newModel2"]

