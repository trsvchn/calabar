import sys


def drive():
    pass


def auth():
    pass


module = type(sys)("google.colab")
module.drive = drive
module.auth = auth
sys.modules["google.colab"] = module

NVIDIA_PATH = '/dev/nvidia0'

# testing installing via pip
TEST_PACKAGE_VALID = 'pip pip'
TEST_PACKAGE_INVALID_TYPE = ['foo', 'bar']
TEST_PACKAGE_INVALID = 'foo bar'

FROM_ADDR = 'foo@bar'
TO_ADDRS = ['foo@foo', 'bar@bar']
