import pytest
from conftest import *
import sys

from calabar.driveutils import MyDrive, SaveToDrive


@pytest.fixture
def mountcopy():
    """Default init"""
    return MyDrive()


@pytest.fixture
def savetodrive():
    """Default init"""
    return SaveToDrive  # TODO: find a way how to mock gauth


def test_init_mountcopy(mountcopy):
    assert mountcopy.mounting_point == '/drive'


def test_init_savetodrive(savetodrive):
    # TODO: Figure out how to mock authorization
    assert savetodrive
