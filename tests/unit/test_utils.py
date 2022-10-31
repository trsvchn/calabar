from os.path import exists

import pytest

from calabar import utils

from ..conftest import *


@pytest.mark.skipif(not exists(NVIDIA_PATH), reason="Requires NVIDIA driver")
def test_get_gpu_usage_output():
    test_out = utils.get_gpu_usage()
    assert test_out
    assert isinstance(test_out, str)


def test_get_disk_usage_output():
    test_out = utils.get_disk_usage()
    assert test_out
    assert isinstance(test_out, str)


def test_get_distro_descr_output():
    test_out = utils.get_distro_descr()
    assert test_out
    assert isinstance(test_out, str)


def test_current_time_output():
    test_out = utils.current_time()
    assert test_out
    assert isinstance(test_out, str)
