import pytest
import os.path
def test_metadata_file():
    assert os.path.isfile('metadata.json')  == True, "Test passed"