from datetime import date

from fastapi import Form, UploadFile, File, HTTPException
from pydantic import BaseModel, field_validator

from apps.accounts.validators import (
    validate_image,
    validate_gender,
    validate_birth_date
)

class ProfileCreateRequestSchema(BaseModel):
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
    ) -> "ProfileCreateRequestSchema":
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


class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    gender: str
    date_of_birth: date
    info: str
    avatar: str
