import pytest
from ..conftest import *
from calabar.install import pip_install, upgrade_pytorch


@pytest.fixture
def install():
    """Installing packages via pip"""
    return pip_install


@pytest.fixture
def upgrade():
    """Upgrading pytorch via pip"""
    return upgrade_pytorch


def test_pip_install_valid(install):
    assert install(TEST_PACKAGE_VALID) == 0


def test_pip_install_invalid_input_type(install):
    with pytest.raises(ValueError):
        install(TEST_PACKAGE_INVALID_TYPE)


def test_pip_install_invalid_input_package(install):
    assert install(TEST_PACKAGE_INVALID) is None


def test_upgrage_pytorch(upgrade):
    assert upgrade() == 0
