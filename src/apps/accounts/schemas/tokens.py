from pydantic import BaseModel, EmailStr


class TokenPairRequestSchema(BaseModel):
    email: EmailStr
    password: str


class TokenPairResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenAccessRequestSchema(BaseModel):
    refresh_token: str


class TokenAccessResponseSchema(BaseModel):
    access_token: str
