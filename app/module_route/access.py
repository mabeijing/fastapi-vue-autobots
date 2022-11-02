# @Time 2022/11/2 14:23
# Author: beijingm

from fastapi import APIRouter
from pydantic import BaseModel, Field

access = APIRouter(prefix="/access")


class UserModel(BaseModel):
    id: int = Field(example=10)


@access.get("/users", )
def users():
    return "hello"
