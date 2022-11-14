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


"""
docker run -d --name mongodb --restart always --net=yapi -p 2717:27017 -v /mongo/data:/data/db -e MONGO_INITDB_DATABASE=yapi -e MONGO_INITDB_ROOT_USERNAME=yapipro -e MONGO_INITDB_ROOT_PASSWORD=yapipro1024 mongo:4.2.21



db.createUser({
  user: 'yapi',
  pwd: 'yapi123456',
  roles: [
 { role: "dbAdmin", db: "yapi" },
 { role: "readWrite", db: "yapi" }
  ]
});


 docker run -d --rm --name yapi-init --link mongodb:mongo --net=yapi -v /home/ubuntu/docker/mongo/conf/config.json:/yapi/config.json yapipro/yapi:1.9.5 server/install.js
 
  
docker run -d --name yapi --link mongodb:mongo --restart always --net=yapi -p 3000:3000 -v /home/ubuntu/docker/mongo/conf/config.json:/yapi/config.json yapipro/yapi:1.9.5 server/app.js
"""