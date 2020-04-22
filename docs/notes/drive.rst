Working with Google Drive
=========================


Mounting
--------

To mount your Google Drive, use this:
::

   from calabar import MyDrive

   drive = MyDrive()
   drive.mount()

By default it mounts to ``/drive``. But Colab utility ``drive`` (which is under the hood) adds additional ``My Drive``
folder thus, the actual path to your Drive content will be ``/drive/My Drive``.

To change the mounting pass the your desired location to ``MyDrive``:

::

    drive = MyDrive(mounting_point='/path')
    drive.mount()

Now your Drive will be mounted to ``/location/My Drive``.


Copying from Drive
------------------

If you need to copy a file or a folder from your (now mounted) Drive to your Colab instance use the ``cp`` method:

::

    file2copy = '/drive/My Drive/data.tar'
    destination = '/content'

    drive.cp(file2copy, destination)


Copying to Drive
------------------

To copy file from Colab to Google Drive:
::

    from calabar import SaveToDrive

    export = SaveToDrive()  # should be initialized once

    export.to_drive('file_on_colab')
    export.to_drive('another_file')