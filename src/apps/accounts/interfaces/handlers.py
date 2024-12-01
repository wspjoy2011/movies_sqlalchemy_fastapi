from abc import ABC, abstractmethod


class InterfaceAvatarFileHandler(ABC):
    @abstractmethod
    def create_directories(self) -> None:
        pass

    @abstractmethod
    def save_file(self, filename: str, content: bytes) -> str:
        pass

