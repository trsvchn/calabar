r"""
Utils are utils.
"""

import subprocess
from datetime import datetime
from sys import version_info as v


def run_cmd(cmd: str) -> str:
    r"""Executes and returns custom command output."""
    return subprocess.getoutput(cmd)


def get_gpu_usage() -> str:
    r"""Returns current gpu usage."""
    cmd_used = "nvidia-smi --query-gpu=memory.used --format=csv,nounits,noheader"
    cmd_total = "nvidia-smi --query-gpu=memory.total --format=csv,noheader"
    return f"{run_cmd(cmd_used)} / {run_cmd(cmd_total)}"


def get_disk_usage() -> str:
    r"""Returns disk total disk usage."""
    cmd = 'df -h --total --output=source,size,used,avail | grep -E "Filesystem|total"'
    return run_cmd(cmd)


def get_distro_descr() -> str:
    r"""Returns Ubuntu distro info."""
    cmd = "cat /etc/*release | grep DISTRIB_DESCRIPTION | cut -d= -f2"
    return run_cmd(cmd).strip('"')


def current_time() -> str:
    r"""Returns current time."""
    return f"{datetime.now():%Y-%m-%d-%H-%M}"


def get_gpu_name() -> str:
    r"""Returns GPU name."""
    cmd = "nvidia-smi --query-gpu=name --format=csv,noheader"
    return run_cmd(cmd)


def get_cuda_version() -> str:
    r"""Returns CUDA version."""
    cmd = "cat /usr/local/cuda/version.txt"
    return run_cmd(cmd)


def get_cudnn_version() -> str:
    r"""Returns CUDA version.

    TODO: Check this ones:
    cat /usr/include/cudnn.h | grep "define CUDNN_MAJOR"
    cat /usr/include/cudnn.h | grep "define CUDNN_MINOR"
    cat /usr/include/cudnn.h | grep "define CUDNN_PATCHLEVEL"
    """
    cmd = 'python -c "import torch; print(torch.backends.cudnn.version())"'
    return run_cmd(cmd)


def get_python_version() -> str:
    r"""Returns installed python version."""
    return f"Python {v.major}.{v.minor}.{v.micro}"


def get_python_version2() -> str:
    r"""Returns installed python version."""
    cmd = "python -V"
    return run_cmd(cmd)


def get_pytorch_version() -> str:
    r"""Returns installed pytorch's packages version."""
    cmd = "pip list | grep torch"
    return run_cmd(cmd)


def print_sysinfo() -> None:
    r"""Prints general system and pytorch version info."""
    _ = list()
    _.append("OS\t\t\t " + get_distro_descr())
    _.append("----")
    _.append("GPU\t\t\t " + get_gpu_name())
    _.append("CUDA\t\t\t " + get_cuda_version())
    _.append("cuDNN\t\t\t " + ".".join([i for i in get_cudnn_version()]))
    _.append("----")
    _.append("\t\t\t ".join(get_python_version2().lower().split(" ")))
    _.append(get_pytorch_version())
    print(*_, sep="\n")
