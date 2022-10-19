from enum import Enum
from typing import Union

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserIn(UserBase):
    password: str = Field(min_length=3, max_length=15)


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def hash_password(password: str):
    return "secret" + password


def save_user_in_db(user_in: UserIn):
    password = hash_password(user_in.password)
    saved_user = UserInDB(**user_in.dict(), hashed_password=password)
    print("save user.... Not really :P", saved_user)
    return saved_user


app = FastAPI()


@app.get("/")
def hello_world():
    return "hello world"


@app.post("/save/user", response_model=UserOut)
def save_user(user_in: UserIn):
    user = save_user_in_db(user_in)
    return user


class ItemBase(BaseModel):
    name: str
    description: str


class PlaneItem(ItemBase):
    type: str = "plane"


class CarItem(ItemBase):
    type: str = "car"


class ValidType(str, Enum):
    type: str = "plane"
    type2: str = "car"


@app.get("/item", response_model=Union[CarItem, PlaneItem])
def get_item(item_name: ValidType):
    item_value: CarItem | PlaneItem | None = None
    dummy_data = {"name": "string", "description": "string"}
    if item_name == "plane":
        item_value = PlaneItem(**dummy_data, type=item_name)
    else:
        item_value = CarItem(**dummy_data, type=item_name)
    return item_value


if __name__ == "__main__":
    uvicorn.run("response_modal:app", host="localhost", port=8000, reload=True)
