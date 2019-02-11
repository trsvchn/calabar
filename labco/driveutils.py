r"""
Performs mounting, copying and saving files to Google Drive.
"""

import os
import shutil
import errno

from google.colab import auth
from google.colab import drive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from oauth2client.client import GoogleCredentials


class MyDrive:
    r"""
    Use this class to mount your Google Drive and copy folder or files to Colab instance.

    Parameters:
        **mounting_point** (`str`): Place where your Google Drive will be mounted to.

    .. note::
        By default mounts to `/drive`
    """

    def __init__(self, mounting_point: str = '/drive'):
        r"""
        Basic init.

        **mounting_point** (`str`): destination where to mount drive

        Default: '/drive'.
        """
        self.mounting_point = mounting_point

    def mount_drive(self) -> None:
        r"""
        Mounts Drive to specified location.

        """
        drive.mount(self.mounting_point)
        print(f'Google drive mounted on {self.mounting_point}')
        self.mounting_point = os.path.join(self.mounting_point, 'My Drive')

    def copy_from_drive(self, source: str, dest: str) -> None:
        r"""
        Copies file or folder from mounted folder.

        Parameters:
            **source** (`str`): File or folder on mounted drive to copy. Ex: data.tar.gz
            You don't need to specify the full path /drive/My Drive/data.tar.gz, just point file/folder
            starting from your drive without path to mounting point. Simply treat your mounted drive as
            usual drive in cloud. Path to mounting point will add automatically.

            **dest** (`str`): destination path on Colab instance.

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
        r"""Mounts and copies file or folder in one line."""

        self.mount_drive()
        self.copy_from_drive(source, dest)


class SaveToDrive:
    r"""
    Provides authorization to Google Drive and uploads files to it.

    .. note::
        Adopted from Google Colaboratory Code snippets.
    """

    def __init__(self):
        r"""Authorization Step"""
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        self.drive = GoogleDrive(gauth)

    def to_drive(self, file: str) -> None:
        r"""
        Save file from Colab instance directly to Google Drive.

        Parameters:
            **file** (`str`): File to upload. The full path to the file should be specified.
        """

        file_name = os.path.basename(file)
        print(f'Uploading {file_name}...')
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        self.drive = GoogleDrive(gauth)

        uploaded = self.drive.CreateFile({'title': f'{file_name}'})
        uploaded.SetContentFile(f'{file}')
        uploaded.Upload()
        new_file_id = uploaded.get('id')
        print(f'{file_name} Successfully Uploaded. File ID: {new_file_id}')  # print some info
