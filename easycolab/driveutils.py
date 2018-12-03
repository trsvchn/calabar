"""
Performs mounting, copying an saving files to Google Drive
"""

import os
import shutil
import errno
from google.colab import drive


class MountCopy:
    """Mount your Google drive and copy folder/files"""

    def __init__(self, mounting_point: str = '/drive'):
        """
        :param mounting_point: destination where to mount drive
        Default: '/drive'
        """
        self.mounting_point = mounting_point

    def mount_drive(self) -> None:
        """
        Mounts Drive to specified location.
        :return: None
        """
        drive.mount(self.mounting_point)
        print(f'Google drive mounted on {self.mounting_point}')
        self.mounting_point = os.path.join(self.mounting_point, 'My Drive')
        print(self.mounting_point)

    def copy_from_drive(self, source: str, dest: str) -> None:
        """
        Copies file or folder from mounted folder.
        :param source: str, file or folder from drive to be copied. Ex: data.tar.gz
        You don't need to specify the full path /drive/My\ Drive/data.tar.gz, just point file/folder
        from your mounting point
        :param dest: str, destination path
        :return: None

        Adapted from:
        https://www.pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/
        """
        source_path = os.path.join(self.mounting_point, source)
        try:
            shutil.copytree(source_path, dest)
            print(f'Directory {source_path} copied to {dest} successfully')
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(source_path, dest)
                print(f'File {source_path} copied to {dest} successfully')
            else:
                print(f'Failed to copy directory. Error: {e}')

    def __call__(self, source: str, dest: str) -> None:
        """
        Mounts and copies file/folder in one line
        :param mounting_point:
        :param source: str, file or folder from drive to be copied. Ex: data.tar.gz
        :param dest: str, destination path
        :return: None
        """
        self.mount_drive()
        self.copy_from_drive(source, dest)
