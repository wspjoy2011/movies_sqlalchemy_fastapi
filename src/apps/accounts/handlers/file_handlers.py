import os
import uuid
from pathlib import Path

from apps.accounts.handlers.interfaces import InterfaceAvatarFileHandler


class AvatarFileHandler(InterfaceAvatarFileHandler):
    def __init__(self, media_profile_dir: Path):
        self.media_profile_dir = media_profile_dir
        self.create_directories()

    def create_directories(self) -> None:
        if not self.media_profile_dir.exists():
            self.media_profile_dir.mkdir(parents=True)

    def save_file(self, filename: str, content: bytes) -> str:
        filename, extension = os.path.splitext(filename)
        unique_filename = f'{filename}_{uuid.uuid4().hex}{extension}'
        file_path = self.media_profile_dir / unique_filename
        with open(file_path, 'wb') as f:
            f.write(content)
        return unique_filename
