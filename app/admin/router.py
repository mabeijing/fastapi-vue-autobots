# 模块路由文件
from typing import Optional

from fastapi import APIRouter

from enum import Enum


admin = APIRouter()


class ProductType(str, Enum):
    gitlab = 'Gitlab'
    singleton = 'Singleton'
    perforce = 'Perfore'


@admin.get("/")
def index():
    """
    首页
    """
    return {"returnCode": 0}


@admin.get("/user/list")
async def user_list():
    """
    用户列表
    """
    return {"returnCode": 0, "users":
            [
                {"name": "beijing"},
                {"name": "tianjin"}
            ]}


@admin.get("/user/{user_id}")
async def user(user_id: int):
    """
    用户详情
    """
    return {"item": user_id}


@admin.get("/product_type/{product_type}")
def product_type(product_type: ProductType):
    """
    测试Enum类型
    """
    return {"product_type": product_type}
