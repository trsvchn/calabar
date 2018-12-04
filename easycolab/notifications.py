"""
Notifications module
"""

import os
import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Email:
    """
    Notification over email using Gmail account (gmail smtp server).

    Note: Allow “less secure apps” on your Gmail: https://www.google.com/settings/security/lesssecureapps
    """
    def __init__(self, from_addr: str, to_addrs: list):
        """

        :param from_addr (str): Gmail mail address, that will be used as smtp server.
                            All messages will be sent from this account.
        :param to_addrs (list): List of email to send to.
        """
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.pswd = getpass.getpass(f'Password ({self.from_addr}): ')

    def send_mail(self, msg_subject: str, msg_body: str, attachment: str = None):
        """

        :param msg_subject: Message subject, str.
        :param msg_body: str, Message body.
        :param attachment: str, Path to file to be attached. Currently only images are supported.
        :return:
        """
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = ','.join(self.to_addrs)
        msg['Subject'] = msg_subject
        msg.attach(MIMEText(msg_body, 'plain'))

        if attachment:
            _attachment = open(attachment, 'rb').read()
            image = MIMEImage(_attachment, name=os.path.basename(attachment))
            msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.from_addr, self.pswd)
        text = msg.as_string()
        server.sendmail(self.from_addr, self.to_addrs, text)
        server.quit()
