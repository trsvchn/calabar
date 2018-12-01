"""
Handles installation of libraries, packages etc.
"""

from os.path import exists
import subprocess
from wheel.pep425tags import get_abbr_impl, get_impl_ver, get_abi_tag
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class Install:

    def __init__(self):
        self.accelerator = 'cpu'  # default is CPU
        self.platform = None
        self.cuda_version = None
        self.nvidia_device = '/dev/nvidia0'

    def _set_gpu_accelerator(self) -> None:
        """
        Set CUDA version.
        """
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
        """
        Set instance platform info.
        """
        self.platform = f'{get_abbr_impl()}{get_impl_ver()}-{get_abi_tag()}'
        logging.info(f'{self.platform} platform detected!')

    def _pip_install(self, packages: list) -> [int, None]:
        """
        Install listed packages using pip.
        Not really useful for external usage.
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

    def __init__(self):
        super(InstallPyTorch, self).__init__()
        self.link = f'http://download.pytorch.org/whl/'
        self.default_version = '0.4.1'
        self.install = True

    def _get_user_input(self) -> str:
        return str(input())

    def _check_version(self, version: str) -> None:
        """
        Check the correctness of user specified version.
        :param version: string version of PyTorch. Recommended version is 0.4.1.
        :return:
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
        """

        :param version:
        :param gpu:
        :return:
        """

        logging.info('Launching Installation Process...')

        if not version:
            version = self.default_version
        if gpu:
            self._set_gpu_accelerator()
            self._check_version(version)
        if self.install:
            logging.info(f'{version} PyTorch is going to be installed')
            self._set_platform()
            pytorch_wheel = f'torch-{version}-{self.platform}-linux_x86_64.whl'  # setting PyTorch wheel
            logging.info(f'Downloading {pytorch_wheel} from {self.link}\n...')
            pytorch = f'{self.link}{self.accelerator}/{pytorch_wheel}'
            packages = [pytorch, 'torchvision']
            self._pip_install(packages)  # Installing PyTorch and torchvision


def testimport():
    return 42
