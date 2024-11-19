from enum import Enum

from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field, model_validator

app = FastAPI()


class UserType(str, Enum):
    USER = "user"
    ADMIN = "admin"


@app.get("/")
async def hello_world():
    return {"hello": "world"}


# @app.get("/users/{user_id}/")
# async def get_user(user_id: int):
#     return {"id": user_id}


@app.get("/users/{user_type}/{user_id}")
async def get_user(user_type: UserType, user_id: int):
    return {"type": user_type, "id": user_id}


@app.get("/users/{user_id}/")
async def get_user(
        user_id: int = Path(
            ...,
            ge=1,
            description="User ID greater than or equal to 1",
            example=1
        )
):
    return {"id": user_id}


# @app.get("/users/")
# async def get_user(
#         page: int = Query(1, gt=0),
#         size: int = Query(10,le=20)):
#     return {"page": page, "size": size}


# @app.post("/users/")
# async def create_user(name: str = Body(...), age: int = Body(...)):
#     return {"name": name, "age": age}

class User(BaseModel):
    name: str = Field(
        ...,
        pattern="^[a-zA-Z]+$",
        description="Name must contain only English letters (a-z, A-Z)",
        examples=["John"]
    )
    age: int = Field(
        ...,
        ge=18,
        le=66,
        description="Age of the user (must be between 18 and 66)",
        examples=[25]
    )

    @model_validator(mode='before')
    @classmethod
    def preprocess_name(cls, values):
        if 'name' in values and isinstance(values['name'], str):
            values['name'] = values['name'].strip().capitalize()
        return values


class Company(BaseModel):
    name: str = Field(
        ...,
        pattern=r"^[a-zA-Z]+(-[a-zA-Z]+|\s[a-zA-Z]+)?$",
        description="Name must be one word or two words separated by a space or hyphen",
        examples=["Company", "Huge Company", "Huge-Company"]
    )

@app.post("/users/")
async def create_user(user: User, company: Company):
    return {"user": user, "company": company}

