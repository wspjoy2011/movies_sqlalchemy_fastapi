from datetime import date
from typing import NamedTuple


class UserProfileCreateDTO(NamedTuple):
    user_id: int
    gender: str
    date_of_birth: date
    info: str
    avatar_filename: str
    avatar_content: bytes


class UserProfileDTO(NamedTuple):
    id: int
    user_id: int
    gender: str
    date_of_birth: date
    info: str
    avatar: str
