from importlib import util

def test_import_extract():
    spec = util.find_spec("moulinette.extract")
    assert spec is not None, "Failed to import extract module"
