from apps.accounts.interfaces import InterfaceEmailSender


class FakeEmailSender(InterfaceEmailSender):
    def __init__(self):
        self.sent_emails = []

    async def send_activation_email(self, email: str, activation_link: str, fullname: str) -> None:
        self.sent_emails.append({
            "email": email,
            "activation_link": activation_link,
            "fullname": fullname,
        })
