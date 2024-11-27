from datetime import date

from fastapi import Form, UploadFile, File, HTTPException
from pydantic import BaseModel, field_validator, EmailStr

from apps.accounts.validators import (
    validate_username,
    validate_password_strength,
    validate_name,
    validate_image, validate_gender, validate_birth_date)


class UserCreateSerializer(BaseModel):
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


class UserResponseSerializer(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool


class ProfileCreateSerializer(BaseModel):
    gender: str
    date_of_birth: date
    info: str
    avatar: UploadFile

    @classmethod
    def from_form(
        cls,
        gender: str = Form(...),
        date_of_birth: date = Form(...),
        info: str = Form(...),
        avatar: UploadFile = File(...)
    ) -> "ProfileCreateSerializer":
        return cls(gender=gender, date_of_birth=date_of_birth, info=info, avatar=avatar)

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, avatar: UploadFile) -> UploadFile:
        try:
            validate_image(avatar)
            return avatar
        except ValueError as exception:
            raise HTTPException(status_code=400, detail={
                "field": "avatar",
                "message": str(exception)
            })

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, gender: str) -> str:
        try:
            validate_gender(gender)
            return gender
        except ValueError as exception:
            raise HTTPException(status_code=400, detail={
                "field": "gender",
                "message": str(exception)
            })

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, date_of_birth: date) -> date:
        try:
            validate_birth_date(date_of_birth)
            return date_of_birth
        except ValueError as exception:
            raise HTTPException(status_code=400, detail={
                "field": "date_of_birth",
                "message": str(exception)
            })


class ProfileResponseSerializer(BaseModel):
    id: int
    user_id: int
    gender: str
    date_of_birth: date
    info: str
    avatar: str


class TokenPairRequestSerializer(BaseModel):
    email: EmailStr
    password: str


class TokenPairResponseSerializer(BaseModel):
    access_token: str
    refresh_token: str


class TokenAccessRequestSerializer(BaseModel):
    refresh_token: str


class TokenAccessResponseSerializer(BaseModel):
    access_token: str
