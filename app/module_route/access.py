# @Time 2022/11/2 14:23
# Author: beijingm

import time
from fastapi import APIRouter, Path, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from fastapi import exception_handlers
from pydantic import BaseModel, BaseConfig, Field, EmailStr, PrivateAttr, root_validator, validator
import orjson
from typing import Optional

from app.module_route import schema

access = APIRouter(prefix="/access", default_response_class=ORJSONResponse)


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps

    # # 超高端操作，全局验证其。value是每一条UserModelOut数据。
    # @root_validator
    # def validate_value(cls, value: dict):
    #     # {'username': 'beijingm', 'user_id': 100100100, 'custom_id': 100, 'nickname': '大帅', 'avatar': None, 'telephone': '18651815400', 'email': '58149279@qq.com'}
    #     if value == "":
    #         return None
    #     else:
    #         return value


class UserModelOut(OrmBaseModel):
    username: str = Field(default="lisa", description="用户名", title="USERNAME")
    user_id: int
    custom_id: int
    nickname: str = ""
    avatar: Optional[str] = Field(default="", description="用户头像", title="USERNAME")
    telephone: int
    email: EmailStr
    role: int
    status: int
    province: str = ""
    city: str = ""
    county: str = ""
    address: str = ""
    address_detail: str = ""

    # validator可以接收当前类已存在的字段，作为校验字段
    # pre说明在所有验证规则之前验证
    @validator("avatar", pre=True, always=True)
    def validate_date(cls, value):
        if value == "":
            return None
        else:
            return value


class UserModelIn(OrmBaseModel):
    username: str = Field(..., description="用户名", title="USERNAME", example="lisa", repr=False)
    password: str = Field(..., description="密码", title="PASSWORD", example="*****", repr=False)

    nickname: str = Field(default="小帅", description="用户昵称", title="NICKNAME", repr=False)
    avatar: str = ""
    telephone: int
    email: EmailStr

    province: str = ""
    city: str = ""
    county: str = ""
    address: str = ""


@access.get("/users", response_model=list[UserModelOut])
async def users():
    return await schema.AsyncUserCURD.select_users()


# @access.get("/users", response_model=list[UserModel])
# def users():
#     return schema.SyncUserCURD.select_user()

@access.get("/user/{user_id}", response_model=UserModelOut)
async def user(user_id: int = Path(..., example=100100100)):
    sql = schema.select(schema.TbUsers).where(schema.TbUsers.user_id == user_id)
    return await schema.AsyncUserCURD.select_user(sql)


@access.post("/user/add", response_model=UserModelOut)
async def add_user(user: UserModelIn = Body()):
    exist_user: schema.TbUsers = await schema.AsyncUserCURD.select_user_by_model(user)
    if exist_user:
        raise HTTPException(status_code=404, detail="234")

    u = user.dict()
    u.update({"user_id": int(time.time() * 10000000), "custom_id": int(time.time() * 10000000)})
    tb_user = schema.TbUsers(**u)
    _user: schema.TbUsers = await schema.AsyncUserCURD.add_user(tb_user)
    return _user
