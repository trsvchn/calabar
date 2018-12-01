import pytest
from conftest import *


def test_default_install(default_install):
    assert default_install.accelerator == 'cpu'
    assert default_install.platform is None
    assert default_install.cuda_version is None
    assert default_install.nvidia_device == NVIDIA_PATH


def test_set_gpu_accelerator(default_install):
    default_install._set_gpu_accelerator()
    assert default_install.cuda_version == CUDA_VERSION
    assert default_install.accelerator == GPU_ACCELERATOR


def test_pip_install_valid(default_install):
    assert default_install._pip_install(TEST_PACKAGE_VALID) == 0


def test_pip_install_invalid_input_type(default_install):
    with pytest.raises(AssertionError):
        default_install._pip_install(TEST_PACKAGE_INVALID_TYPE)


def test_pip_install_invalid_input_package(default_install):
    assert default_install._pip_install(TEST_PACKAGE_INVALID) is None
