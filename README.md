# CoUtils (Work in progress...)

Useful tools to make Colab more handy.

## Installation

```
!pip install git+https://github.com/tsavchyn/coutils.git
```

## Usage

### Working with Google Drive

Mount your drive:

```python
from coutils import MyDrive

drive = MyDrive('/drive')
drive.mount()
```

Copy file/folder from mounted Drive, for example, some data, model checkpoint from the previous training, etc:

```python
file2copy = '/drive/My Drive/data.tar'
dest = '/content'

drive.cp(file2copy, dest)
```

**NOTE:** During mounting internal colab tool will create 'My Drive' folder inside `/drive`,
so don't forget to add 'My Drive' to file path.

Export file from Colab to Drive, for example, training logs, model checkpoints, etc:

```python
from coutils import SaveToDrive

export = SaveToDrive()

export.to_drive('file_on_colab')
export.to_drive('another_file')
```

**NOTE:** Simply copying to mounted Drive would lead to nothing.

### Working with Archives

Currently `tar`/`tar.gz` and `zip` archives extracting are supported.

```python
from coutils import untar

untar('data.tar', 'to_destination')
```

```python
from coutils import unzip

unzip('data.zip', 'to_destination')
```

### Sending Notifications over Gmail

**NOTE:** To use this option, you need to allow “less secure apps” on your Gmail account:
> https://www.google.com/settings/security/lesssecureapps

**SECURITY WARNING:** Continuous sending of emails (for example, sending email after each epoch) requires storing your 
Gmail account password in memory, allowing you not to relogin to SMTP server each time, when you want to send an email.
BUT, CoUtils uses secure TLS connection. Anyway, if you feel unsafe because of "less secure appps" and using
SMTP server, or you just don't like it, you may not use it or use another "less secured" account
(with "less secure apps” option on) and send emails to your primary account, as shown below:

```python
from coutils import Email

from_addr = 'johndoe@gmail.com'  # email with "allow less secure", this account's SMTP server will be used as a sender
to_addrs = ['another@gmail.com',]  # a list of receivers

email = Email(from_addr, to_addrs)

msg_subject = 'Subject of the email'
msg_body = 'Email body.'

email.send(msg_subject, msg_body)
```

### Misc

```python
from coutils.utils import *

# Get current GPU RAM usage:

print(get_gpu_usage())

# Get disk usage:

print(get_disk_usage())

# Get current time as formatted string in %Y-%m-%d-%H-%M:

print(current_time())

# Get distro description:

print(get_distro_descr())
```

## Complete Usage Example

The following example shows up how to integrate CoUtils with your training pipeline.

```python
from coutils import MyDrive, SaveToDrive, untar, unzip, Email
from coutils.utils import *


# Authorize to Drive to allow mounting
drive = MyDrive('/drive')
drive.mount()

# Authorize to Drive to to allow exporting | NOTE: you can use here another Drive
export = SaveToDrive()

from_addr = 'johndoe@gmail.com'
to_addrs = ['another@gmail.com']

email = Email(from_addr, to_addrs)

# Prepare your data 

# Copy your data:
drive.cp('/drive/My Drive/data.tar', '/content')

# Untar/unzip it:
untar('/content/data.tar', '/content')

# ...
# Model definition, training, validation functions etc...
# ...

# Main loop:

# Notification about beginning of the model training process 

start_sub = 'Starting training...'
start_msg = f'Training (your model descr) has started at {current_time()}\
            \nCurrent GPU usage: {get_gpu_usage()}\
            \nCurrent disk usage: {get_disk_usage()}'

email.send(start_sub, start_msg)

for epoch in n_epochs:
    train_loss, train_acc = train(...)
    val_loss, val_ acc = validate(...)
      
    # Here you're saving your model checkpoint
    checkpoint_name = f'{epoch}-{val_loss}-{acc}-mymodel.checkpoint'  # this is just example
    save_checkpoint(f'/content/checkpoints/{checkpoint_name}')
    
    # Here you're loading it to your Drive:
    export.to_drive(f'/content/checkpoints/{checkpoint_name}')
    
    # Epoch is over, model checkpoint is exported to your drive, let's notify you about current success:
    
    epoch_sub = f'{epoch}/{n_epoch} has finished!'
    epoch_msg = f'{epoch}/{n_epoch} has finished successfully at {current_time()}\
                \ntrain_loss: {train_loss} | val_loss: {val_loss} | train_acc: {train_acc} | val_acc: {val_ acc}\
                \nModel checkpoint {checkpoint_name} successfully loaded to Drive\
                \nCurrent GPU usage: {get_gpu_usage()}\
                \nCurrent disk usage: {get_disk_usage()}'

    email.send(epoch_sub, epoch_msg)
    
# Notification email about model training completion.

end_sub = 'Training has finished!'
end_msg = f'Training (your model descr) has finished at {current_time()}\
            \nCurrent GPU usage: {get_gpu_usage()}\
            \nCurrent disk usage: {get_disk_usage()}'

email.send(end_sub, end_msg)
```

## TODO:

* tar/zip archiving
* More docs
* More examples
