# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()


NAME = "calabar"
DESCRIPTION = "Makes Google Colab more friendly."
LICENSE = "Apache-2.0"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"
REQUIRED = [
    "pydrive",
]
EXCLUDE = ("tests", "docs", "notebooks")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    license=LICENSE,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=EXCLUDE),
    install_requires=REQUIRED,
)
