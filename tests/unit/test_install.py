from os.path import exists
import pytest
from conftest import *


def test_default_install(install):
    assert install.accelerator == 'cpu'
    assert install.platform is None
    assert install.cuda_version is None
    assert install.nvidia_device == NVIDIA_PATH


@pytest.mark.skipif(not exists(NVIDIA_PATH), reason='Requires CUDA')
def test_set_gpu_accelerator(install):
    install._set_gpu_accelerator()
    assert install.cuda_version == CUDA_VERSION
    assert install.accelerator == GPU_ACCELERATOR


def test_pip_install_valid(install):
    assert install._pip_install(TEST_PACKAGE_VALID) == 0


def test_pip_install_invalid_input_type(install):
    with pytest.raises(AssertionError):
        install._pip_install(TEST_PACKAGE_INVALID_TYPE)


def test_pip_install_invalid_input_package(install):
    assert install._pip_install(TEST_PACKAGE_INVALID) is None
