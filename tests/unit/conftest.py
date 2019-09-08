import sys
import pytest

sys.path.append('.')  # for pytest on automatic testing stage
sys.modules['google'] = __import__('mock_import')
sys.modules['google.colab'] = __import__('mock_import')


NVIDIA_PATH = '/dev/nvidia0'


# testing installing via pip
TEST_PACKAGE_VALID = 'pip pip'
TEST_PACKAGE_INVALID_TYPE = ['foo', 'bar']
TEST_PACKAGE_INVALID = 'foo bar'


FROM_ADDR = 'foo@bar'
TO_ADDRS = ['foo@foo', 'bar@bar']
