r"""Utils is utils."""

import subprocess
from datetime import datetime


def get_gpu_usage() -> str:
    r"""Returns current gpu usage."""
    # TODO: collect usage statistics on time intervals?
    used = subprocess.getoutput('nvidia-smi --query-gpu=memory.used --format=csv,nounits,noheader')
    total = subprocess.getoutput('nvidia-smi --query-gpu=memory.total --format=csv,noheader')
    return f'{used} / {total}'


def get_disk_usage() -> str:
    r"""Returns disk total disk usage."""
    info = subprocess.getoutput('df -h --total --output=source,size,used,avail | grep -E "Filesystem|total"')
    return info


def get_distro_descr() -> str:
    r"""Returns Ubuntu distro info."""
    distro = subprocess.getoutput('cat /etc/*release | grep DISTRIB_DESCRIPTION | cut -d= -f2')
    return distro


def current_time() -> str:
    r"""Returns current time."""
    date_time = f'{datetime.now():%Y-%m-%d-%H-%M}'
    return date_time
