# 模块路由文件

from typing import Optional, Set, TYPE_CHECKING
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from fastapi import APIRouter, Body, Path, params, Response

# from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse


from enum import Enum

demo = APIRouter()


class UserType(BaseModel):
    id: Optional[str] = Field(title='ID', default='0', description='IDs')
    name: str


class User(BaseModel):
    """
    支持模型嵌套
    """
    id: UUID = Field(default='6b96e0df-ba85-4007-a667-08e0b454e04b')
    name: str
    type: UserType
    age: int
    email: EmailStr
    register_time: datetime
    birthday: Set[int]
    money: Decimal
    image: HttpUrl

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             # "id": "d2323",
    #             "type": {
    #                 "id": "12",
    #                 "name": "Gitlab"
    #             },
    #             "name": "Foo",
    #             "age": 33,
    #             "email": "58149278@qq.com",
    #             "register_time": "2022",
    #             "birthday": (0,2,3,4),
    #             "money": 12131.4233454565,
    #             "image": "/data/file"
    #         }
    #     }


class ProductType(str, Enum):
    gitlab = 'Gitlab'
    singleton = 'Singleton'
    perforce = 'Perfore'


@demo.post("/order/{order_id:path}")
def order(order_id: str, user: dict[str, User], delete: bool, product_type: ProductType, limit: int = 10):
    """
    1.支持有类型的路径参数 order_id: str\n
    2.支持url路径参数 {order_id:path} 包含/static/xxx.file。\n
    3.通过pydantic构造复合型参数验证,就是body。\n
    4.方法参数如果是str,int,bool,float这样的,就是?param=int&limit=100,如果是dict,就是body。\n
    5.如果存在bool类型,会自动转化成ye,1,on。\n
    6.允许默认值,就是非必填参数。否则就是必填参数。\n
    7.支持原生Enum类型,作为?param=value。
    """
    return {"order_id": order_id, "user": user, "limit": limit, "delete": delete, "product_type": product_type}


@demo.get("/usrs/self", tags=['测试用例'], summary='查询当前用户')
async def user_self():
    return "hello world"


@demo.get("/users/{user_id}")
async def user_by_id(
    user_id: str = Path(max_length=10, deprecated=True)
):
    """
    路径参数。\n
    1.顺序很重要,相同的路由会覆盖
    2.使用Enum类,配置预置参数
    3.不支持默认值,不管是否指定默认值,都是必填字段
    4.包含路径/符号的参数
    """
    return {"user_id": user_id}


@demo.get("/user/{user_id}")
async def user(user_id: int):
    """
    用户详情
    """
    return {"item": user_id}


@demo.get("/product_type/{product_type}")
def product_type(product_type: ProductType):
    """
    测试Enum类型
    """
    return {"product_type": product_type}


@demo.get("/upload/{file_path:path}")
def upload(file_path: str):
    """
    file_path:path 允许url参数接收/ubuntu/file/xxx.json这样/开头的格式。
    路由支持 http://ip:port/upload//ubuntu/file/xxx.json 形式。
    """
    return {"returnCode": 0}


@demo.get("/item")
def query_item(q: int = 0, limit: int = 10):
    """
    路由支持 http://ip:port/item?q=0&limit=10
    """
    return {"q": q, "limit": limit}


@demo.get("/query/{item}")
def item_limit(item: str, limit: Optional[int] = None):
    """
    路由支持 可选参数limit
    """
    return {"item": item, "limit": limit}
