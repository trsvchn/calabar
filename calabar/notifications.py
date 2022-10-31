"""
Notifications module. Currently provides only email notifications.
"""

import getpass
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    r"""
    Notification over email using Gmail account (Gmail SMTP server). Currently tested only on Gmail account.
    But you can try another SMTP servers by replacing default values for ``host`` and ``port``.

    Parameters:
        **from_addr** (`str`): Email address, that will be sender. All messages will be sent from this account. You'll also
        be asked to enter password from your account. SMTP server requires your Gmail password.

        **to_addrs** (`list`): List of email address that will receive messages. List of receiver. You can use the same address
        as for ``from_addr``. In this case the message will be sent and received by the same account.

        **host** (`str`): SMTP server host address. Default: ``'smtp.gmail.com'`` (for Gmail).

        **port** (`int`): SMTP port. Default: ``587`` (for Gmail).

    .. warning::
        If you face some problems with sending emails. Try to allow “less secure apps” on your Gmail:
        https://www.google.com/settings/security/lesssecureapps
    """

    def __init__(self, from_addr: str, to_addrs: list, host: str = "smtp.gmail.com", port: int = 587):
        r"""Default init"""
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.pswd = getpass.getpass(f"Password ({self.from_addr}): ")
        self.host = host
        self.port = port

    def send(self, msg_subject: str, msg_body: str, attachment: str = None):
        r"""
        Sends email with subject ``msg_subject``, text ``msg_body`` and (optional) attachment ``attachment``.

        Parameters:
            **msg_subject** (`str`): Message subject.

            **msg_body** (`str`): Message text content (body).

            **attachment** (`str`): Path to file to be attached.

        .. note::
            Currently only images are supported as file attachments.
        """

        msg = MIMEMultipart()
        msg["From"] = self.from_addr
        msg["To"] = ",".join(self.to_addrs)
        msg["Subject"] = msg_subject
        msg.attach(MIMEText(msg_body, "plain"))

        if attachment:
            _attachment = open(attachment, "rb").read()
            image = MIMEImage(_attachment, name=os.path.basename(attachment))
            msg.attach(image)

        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(self.from_addr, self.pswd)
        text = msg.as_string()
        server.sendmail(self.from_addr, self.to_addrs, text)
        server.quit()
