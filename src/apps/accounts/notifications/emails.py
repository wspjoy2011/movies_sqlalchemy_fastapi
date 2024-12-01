import aiosmtplib
from email.message import EmailMessage

from apps.accounts.interfaces import InterfaceEmailSender


class EmailSenderGmail(InterfaceEmailSender):
    def __init__(self,
                 hostname: str,
                 port: int,
                 email: str,
                 password: str,
                 activation_template: str):
        self._hostname = hostname
        self._port = port
        self._email = email
        self._password = password
        self._activation_template = activation_template

    async def send_activation_email(self, email: str, activation_link: str, fullname: str) -> None:
        message = EmailMessage()
        message["From"] = "admin@company.com"
        message["To"] = email
        message["Subject"] = "Activation Token"

        html_content = self._activation_template.format(fullname=fullname, activation_link=activation_link)
        message.add_alternative(html_content, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=self._hostname,
            port=self._port,
            username=self._email,
            password=self._password,
            use_tls=True
        )
