# @Time 2022/11/2 14:23
# Author: beijingm

import time
from typing import Optional
from pydantic import BaseModel, BaseConfig, Field, EmailStr, validator, PositiveInt

import orjson
from fastapi import APIRouter, Path, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from app.module_route import schema

access = APIRouter(prefix="/access", default_response_class=ORJSONResponse)


class OrmBaseModel(BaseModel):
    class Config(BaseConfig):
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
    # 注意，指定alise的时候，一定要和数据库字段保持一致，否则会导致实例化失败
    username: str = Field(..., description="用户名", title="USERNAME", example="lisa")
    user_id: int = Field(..., description="用户ID", title="USER_ID", example="")
    custom_id: int
    nickname: str = ""
    avatar: Optional[str] = Field(default="", description="用户头像", title="USERNAME")
    telephone: PositiveInt
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
    username: str = Field(..., description="用户名", title="USERNAME", example="lisa")
    password: str = Field(..., description="密码", title="PASSWORD", example="*****")

    nickname: str = Field(default="", description="用户昵称", title="NICKNAME", example="小帅")
    avatar: str = ""
    telephone: PositiveInt = Field(..., description="用户电话", title="TELEPHONE", example=18651815400)
    email: EmailStr

    province: str = ""
    city: str = ""
    county: str = ""
    address: str = ""

    class Config(BaseConfig):
        title = "UserModelIns"  # 可以嵌套定义，这个title用于在swagger上显示schema


@access.get("/users", response_model=list[UserModelOut], response_class=ORJSONResponse)
async def users():
    return await schema.AsyncUserCURD.select_users()


# @access.get("/users", response_model=list[UserModel])
# def users():
#     return schema.SyncUserCURD.select_user()

@access.get("/user/{user_id}", response_model=UserModelOut)
async def user(user_id: int = Path(..., example=100100100)):
    sql = schema.select(schema.TbUsers).where(schema.TbUsers.user_id == user_id)
    user: schema.TbUsers = await schema.AsyncUserCURD.select_user(sql)
    if not user:
        raise HTTPException(status_code=404, detail={"msg": "用户ID不存在"})
    return user


@access.post("/user/add", response_model=UserModelOut)
async def add_user(user: UserModelIn = Body()):
    exist_user: schema.TbUsers = await schema.AsyncUserCURD.select_user_by_model(user)
    if exist_user:
        raise HTTPException(status_code=404, detail={"msg": "用户已存在"})

    u = user.dict()
    u.update({"user_id": int(time.time() * 10000000), "custom_id": int(time.time() * 10000000)})
    tb_user = schema.TbUsers(**u)
    _user: schema.TbUsers = await schema.AsyncUserCURD.add_user(tb_user)
    return _user
