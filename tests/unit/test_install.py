import pytest

from calabar.install import pip_install

from ..conftest import *


@pytest.fixture
def install():
    """Installing packages via pip"""
    return pip_install


def test_pip_install_valid(install):
    assert install(TEST_PACKAGE_VALID) == 0


def test_pip_install_invalid_input_type(install):
    with pytest.raises(ValueError):
        install(TEST_PACKAGE_INVALID_TYPE)


def test_pip_install_invalid_input_package(install):
    assert install(TEST_PACKAGE_INVALID) is None
