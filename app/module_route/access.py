# @Time 2022/11/2 14:23
# Author: beijingm

from fastapi import APIRouter

access = APIRouter(prefix="/access")


@access.get("/users", )
def users():
    return "hello"
