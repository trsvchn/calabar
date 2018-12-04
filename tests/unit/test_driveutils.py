import pytest
from conftest import *
import sys

sys.modules['google'] = __import__('mock_import')
sys.modules['google.colab'] = __import__('mock_import')

from easycolab.driveutils import MountCopy, SaveToDrive


@pytest.fixture
def mountcopy():
    """Default init"""
    return MountCopy()


@pytest.fixture
def savetodrive():
    """Default init"""
    return MountCopy()


def test_init_mountcopy(mountcopy):
    assert mountcopy.mounting_point == '/drive'


def test_init_savetodrive(savetodrive):
    # TODO: Figure out how to mock authorization
    assert savetodrive
