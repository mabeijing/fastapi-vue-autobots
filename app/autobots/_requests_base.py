"""
1. Path
2. Query
3. Body
4. Cookie
5. Header
6. Form and File
7. Background Tasks
8. Static
9. Templates
"""
from enum import Enum
from decimal import Decimal
from typing import Optional, Union

from fastapi import APIRouter
from fastapi import Path, Query, Body, File, Form, UploadFile, Cookie, Header

from pydantic import BaseModel

req_base = APIRouter(prefix="/req_base")


class UserType(str, Enum):
    boss = "BOSS"
    driver = "DRIVER"


class ProductType(BaseModel):
    id: int
    name: str
    money: float


@req_base.get("/path/{path_const}/{path_type}/{path_item:path}")
def path_demo(path_type: UserType, path_item: str):
    """
    1. 所有的Path参数都是必填项。\n
    2. 不支持默认值，配置了也不生效。\n
    3. 支持str, int, Enum, None(不生效), bool, float, 不支持list, dict, BaseModel(等效dict)\n
        3.1 str => string\n
        3.2 int => interger\n
        3.3 float, Decimal => number\n
        3.4 bool => boolean, 默认"true"/"false", 支持[1, "on", "yes"]的大小写形式\n
        3.5 Enum => 基础数据类型\n
        3.6 Union[int, bool] => 支持数字,会覆盖1的形式,并且["on", "yes", "true"]\n
        3.7 Union[str, bool] => 支持字符串, str会覆盖bool\n
        3.8 支持int/str之间的自动解析。
        3.9 Path最好不要用Union和Optional,可能会导致swaggerUI解析失败。\n
        3.10 通过指定`:path`, 参数类型`str`,可以支持`/static/a.properties`这样的路径格式。\n
        3.11 如果试图函数没有路由参数，则{path_type}就当作路由常量而不是必填项。
    """
    return {"path_type": path_type, "path_item": path_item}


class Limit(str, Enum):
    ok = "OK"
    non = "NON"


@req_base.post("/query/{q}")
def query_demo(q: bool, limit: Optional[Limit] = None, extra: int = 40):
    """
    1. Query是视图函数内不在Path内的参数,并且参数必须是int,float,bool,str,Enum这样的基础类型。
    2. 不区分http动词。
    3. 支持可选
    4. 支持默认值
    """
    return {"q": q, "limit": limit, "extra": extra}


class Product(BaseModel):
    product_id: int
    product_name: str


@req_base.post("/body")
def body_demo(product: Product):
    """
    Body是视图函数内不在Path内的参数,类似Query。但是Query是基础数据类型,Body是dict, list数据类型。
    1. 有Body参数的,不能用get。
    2. 支持默认值, Union[Product, None] = None 允许body=null
    """
    return {"product": product}


@req_base.post("/product/new/{product_id}")
def product_new(product_id: float, product: Product, q: bool = False):
    """
    混合参数场景
    """
    return {"product_id": product_id, "product": product, "q": q}
