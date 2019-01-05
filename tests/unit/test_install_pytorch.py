import builtins
import pytest
from conftest import *


def test_pytorch_install_init(install_pytorch):
    assert install_pytorch.accelerator == 'cpu'
    assert install_pytorch.platform is None
    assert install_pytorch.cuda_version is None
    assert install_pytorch.nvidia_device == NVIDIA_PATH
    assert install_pytorch.link == PYTORCH_LINK
    assert install_pytorch.default_version == DEFAULT_PYTORCH_VERSION
    assert install_pytorch.install


def test_get_user_input(monkeypatch, install_pytorch):
    def input_patch():
        return 'foo'
    monkeypatch.setattr(builtins, 'input', input_patch)
    assert install_pytorch._get_user_input() == 'foo'


@pytest.mark.parametrize("version,confirmation,install,cuda", [('0.4.0', 'n', False, DEFAULT_ACCELERATOR),
                                                               ('0.4.0', 'y', True, 'cu91'),
                                                               ('0.4.1', 'y', True, DEFAULT_ACCELERATOR),
                                                               ])
def test_check_version(monkeypatch, install_pytorch, version, confirmation, install, cuda):
    def input_patch():
        return confirmation

    with monkeypatch.context() as m:
        m.setattr(builtins, 'input', input_patch)
        assert install_pytorch.accelerator == DEFAULT_ACCELERATOR
        assert install_pytorch.install is True
        assert install_pytorch._check_version(version) is None
        assert install_pytorch.install is install
        assert install_pytorch.accelerator == cuda


@pytest.mark.skip(reason='Performs installation')
def test_install_pytorch_default(install_pytorch):
    """Test default PyTorch 1.0.0 installation with CUDA support"""
    assert install_pytorch() is None


@pytest.mark.skip(reason='Performs too much installs')
@pytest.mark.parametrize('version,gpu,confirmation,install', [('0.4.0', True, 'n', False),
                                                              ('0.4.0', False, 'n', True),
                                                              ('0.4.0', True, 'y', True),
                                                              ('0.4.0', False, 'y', True),
                                                              ('0.4.1', True, 'y', True),
                                                              ('0.4.1', False, 'y', True),
                                                              ])
def test_call_install_pytorch(monkeypatch, install_pytorch, version, gpu, confirmation, install):
    def input_patch():
        return confirmation

    with monkeypatch.context() as m:
        assert install_pytorch.install is True
        m.setattr(builtins, 'input', input_patch)
        assert install_pytorch(version, gpu) is None
        assert install_pytorch.install is install
