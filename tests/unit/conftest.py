import sys
import pytest

sys.path.append('.')  # for pytest on automatic testing stage

from easycolab.install import Install


DEFAULT_ACCELERATOR = 'cpu'
CORRECT_PLATFORM_3 = 'cp36-cp36m'
CUDA_VERSION = '9.2'
GPU_ACCELERATOR = 'cu92'
NVIDIA_PATH = '/dev/nvidia0'
TEST_PACKAGE_VALID = ['pip', 'pip']
TEST_PACKAGE_INVALID_TYPE = 'foo'
TEST_PACKAGE_INVALID = ['foo', 'bar']




@pytest.fixture
def default_install():
    """Returns a Default install"""
    return Install()


@pytest.fixture
def pytorch_install():
    """Returns a Default install"""
    return Install()