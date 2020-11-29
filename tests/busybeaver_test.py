import busybeaver as bb
import os

FILE_DIR = os.path.dirname(__file__)

# Hut tests
def test_Hut_initialize():

    print(FILE_DIR)
    config_file = os.path.join(FILE_DIR, r"data\test_config.ini")
    testhut = bb.Hut(config_file)
    print(testhut.config_file)

    assert testhut.models == ["newModel1", "newModel2"]