r"""
Handles installation of libraries, packages etc.
"""

from os.path import exists
import subprocess
from wheel.pep425tags import get_abbr_impl, get_impl_ver, get_abi_tag
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class Install:
    r"""Base class for installation stuff."""

    def __init__(self):
        self.accelerator = 'cpu'  # default is CPU
        self.platform = None
        self.cuda_version = None
        self.nvidia_device = '/dev/nvidia0'

    def _set_gpu_accelerator(self) -> None:
        r"""Set right CUDA version."""

        is_cuda = exists(self.nvidia_device)
        assert is_cuda, "No GPU detected. Please change runtime type to 'GPU':\
                         \nRuntime -> Change runtime type -> Hardware accelerator -> GPU"

        cmd = 'ldconfig -p | grep cudart.so'
        cuda = subprocess.getoutput(cmd).split('.')[2:4]
        self.cuda_version = ".".join([i[0] for i in cuda])  # setting the cuda version
        logging.info(f'{self.cuda_version} CUDA version detected!')

        # Set values:
        cuda = 'cu' + ''.join([i[0] for i in cuda])
        self.accelerator = cuda  # set accelerator to GPU

    def _set_platform(self) -> None:
        r"""Set instance platform."""

        self.platform = f'{get_abbr_impl()}{get_impl_ver()}-{get_abi_tag()}'
        logging.info(f'{self.platform} platform detected!')

    def _pip_install(self, packages: list) -> [int, None]:
        r"""
        Install listed packages using pip. Not really useful for external usage.

        Parameters:
            **packages** (`list`): Packages to install as list of strings.
        """

        assert isinstance(packages, list), 'input packages is not a list! Please, provide packages as list of str'

        cmd = f'pip install -q {" ".join(packages)}'
        installation_output = subprocess.call(cmd, shell=True)  # expecting for 0

        if installation_output == 0:
            logging.info(f'The following packages were installed successfully: {" ".join(packages)}')
            return installation_output
        else:
            logging.critical('Error occurred during installation!')
            logging.info(f'To get full error message, run this command in the next cell:\n###\n!{cmd}\n###')  # TODO: refactor!!
            return None


class InstallPyTorch(Install):
    r"""
    .. note::
        This feature is outdated. Colab already supports with PyTorch out of the box.

    Handles PyTorch installation. By default installs PyTorch ``1.0.0`` version compiled with CUDA 9.0.
    In addition, installation of version ``0.4.1``, and version ``0.4.0`` are also available.
    """

    def __init__(self):
        super(InstallPyTorch, self).__init__()
        self.link = f'http://download.pytorch.org/whl/'
        self.nightly_link = 'https://download.pytorch.org/whl/nightly/cu92/torch_nightly.html'
        self.default_version = '1.0.0'
        self.install = True

    def _get_user_input(self) -> str:
        return str(input())

    def _check_version(self, version: str) -> None:
        r"""
        Checks the user specified version. Recommended versions are ``1.0.0`` or ``1.4.1``.
        """

        if version == '0.4.0':
            logging.warning(f'Chosen PyTorch version {version} doesn\'t ship with CUDA {self.cuda_version}')
            logging.warning(f'Recommended PyTorch version for CUDA {self.cuda_version} is {self.default_version}')
            _ = True
            while _:
                logging.warning('Install this version anyway? Type "y" to continue installation or "n" to cancel:')
                confirm = self._get_user_input()
                if confirm:
                    if confirm == 'y':
                        self.accelerator = 'cu' + '91'
                        _ = False
                    elif confirm == 'n':
                        self.install = False
                        logging.info('Installation canceled!')
                        _ = False

    def __call__(self, version: str = None, gpu: bool = True) -> None:
        r"""
        Launch Installation process.

        Parameters:
            **version** (`str`): Version of Pytorch to install. Default: ``1.0.0``
            **gpu** (`bool`): Install with CUDA support, default: ``True``.
        """

        logging.info('Launching Installation Process...')

        if not version:
            version = self.default_version
        if gpu:
            self._set_gpu_accelerator()
            self._check_version(version)
        if self.install:
            logging.info(f'{version} PyTorch is going to be installed')
            if version == '1.0.0':
                pytorch_latest = ['torch', 'torchvision']
                logging.info(f'Downloading PyTorch {version}\n...')
                self._pip_install(pytorch_latest)  # Installing PyTorch and torchvision
            else:
                self._set_platform()
                pytorch_wheel = f'torch-{version}-{self.platform}-linux_x86_64.whl'  # setting PyTorch wheel
                logging.info(f'Downloading {pytorch_wheel} from {self.link}\n...')
                pytorch = f'{self.link}{self.accelerator}/{pytorch_wheel}'
                packages = [pytorch, 'torchvision']
                self._pip_install(packages)  # Installing PyTorch and torchvision


install_pytorch = InstallPyTorch()  # TODO: outdated!!


def upgrade_pytorch():
    r"""Upgrades torch and torchvision to the latest version using pip.
    """
    cmd = 'pip install torch torchvision -U'
    logging.info(f'Upgrading pytorch via {cmd}')
    installation_output = subprocess.call(cmd, shell=True)

    if installation_output == 0:
        logging.info('torch and torchvision were upgraded to the latest version successfully!')
    else:
        logging.critical('Error occurred during installation!')
        logging.info(f'To get full error message, run the following command in the next cell:\n###\n!{cmd}\n###')
