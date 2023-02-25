# 路由文件配置

import requests
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl

from fastapi import APIRouter, Body

api = APIRouter(prefix="/api")


class Methods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class RequestIn(BaseModel):
    method: Methods = Field(Methods.GET, description="method")
    url: HttpUrl = Field()
    headers: dict = Field()
    cookies: dict = Field()
    body: dict = Field()


@api.post("/request")
def do_request(
        request: RequestIn = Body()
):
    return request

