r"""Module for archives unpacking
"""

import tarfile
from zipfile import ZipFile


class Extractor:
    r"""Main class for extracting files from archives"""

    def __init__(self, arch_obj):
        self.arch_obj = arch_obj

    def extract_all(self, path_to_file: str, dest_path: str) -> None:
        r"""
        Extract all files from archive file.

        Parameters:
            **path_to_file** (`str`): Path to archive.

            **dest_path** (`str`): Destination path for files to be extracted.
        """

        if "gz" in path_to_file:
            mode = "r:gz"
        else:
            mode = "r"

        print(f"Extracting files from {path_to_file}...")

        if "tar" in path_to_file:

            with self.arch_obj.open(path_to_file, mode) as zf:
                zf.extractall(dest_path)

        elif "zip" in path_to_file:

            with self.arch_obj(path_to_file, mode) as zf:
                zf.extractall(dest_path)

        print(f"Files successfully extracted to {dest_path}")

    def __call__(self, path_to_file: str, out_path: str):
        self.extract_all(path_to_file, out_path)


unzip = Extractor(ZipFile)
untar = Extractor(tarfile)
