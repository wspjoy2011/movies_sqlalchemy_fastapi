import os

import aiosmtplib
from email.message import EmailMessage

from apps.accounts.email_templates.registrations import REGISTRATION_HTML_CONTENT
from apps.accounts.interfaces import InterfaceEmailSender


class EmailSenderGmail(InterfaceEmailSender):
    def __init__(self):
        self._hostname = os.getenv('EMAIL_HOST')
        self._port = os.getenv('EMAIL_PORT')
        self._email = os.getenv('EMAIL_HOST_USER')
        self._password = os.getenv('EMAIL_HOST_PASSWORD')

    async def send_activation_email(self, email: str, activation_link: str, fullname: str) -> None:
        message = EmailMessage()
        message["From"] = "admin@company.com"
        message["To"] = email
        message["Subject"] = "Activation Token"

        html_content = REGISTRATION_HTML_CONTENT.format(fullname=fullname, activation_link=activation_link)
        message.add_alternative(html_content, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=self._hostname,
            port=self._port,
            username=self._email,
            password=self._password,
            use_tls=True
        )
