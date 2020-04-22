r"""
Handles installation of additional libraries, packages etc.
"""

import subprocess
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def pip_install(packages: str) -> [int, None]:
    r"""
    Install listed packages using pip. Not really useful for external usage.

    Parameters:
        **packages** (`str`): Packages to install in str format separated by space. Ex: 'numpy scipy'.
    """

    if not isinstance(packages, str):
        raise ValueError('Please, provide packages in a str, Ex: "numpy scipy"')
    else:
        packages = packages.strip()

    cmd = f'pip install -q {packages}'
    logging.info(f'Installing {packages}...')
    installation_output = subprocess.call(cmd, shell=True)  # expecting for 0

    if installation_output == 0:
        logging.info(f'The following packages were installed successfully: {packages}')
        return installation_output
    else:
        logging.critical('Error occurred during installation!')
        logging.info(f'To get full error message, run the following command in the next cell:\n###\n!{cmd}\n###')


def upgrade_pytorch():
    r"""Upgrades torch and torchvision to the latest version using pip.
    """
    cmd = 'pip install torch torchvision -U'
    logging.info(f'Upgrading pytorch via {cmd}')
    installation_output = subprocess.call(cmd, shell=True)

    if installation_output == 0:
        logging.info('torch and torchvision were upgraded to the latest version successfully!')
        return installation_output
    else:
        logging.critical('Error occurred during installation!')
        logging.info(f'To get full error message, run the following command in the next cell:\n###\n!{cmd}\n###')
