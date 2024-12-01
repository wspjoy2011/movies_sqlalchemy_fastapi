from pydantic import BaseModel, field_validator, EmailStr

from apps.accounts.validators import (
    validate_username,
    validate_password_strength,
    validate_name,
)


class UserCreateRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @field_validator('username')
    @classmethod
    def validate_username_field(cls, username: str) -> str:
        validate_username(username)
        return username

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name_field(cls, name: str) -> str:
        validate_name(name)
        return name

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, password: str) -> str:
        validate_password_strength(password)
        return password


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
