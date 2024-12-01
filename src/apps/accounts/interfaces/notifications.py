from abc import ABC, abstractmethod


class InterfaceEmailSender(ABC):

    @abstractmethod
    async def send_activation_email(self, email: str, activation_link: str, fullname: str) -> None:
        pass
