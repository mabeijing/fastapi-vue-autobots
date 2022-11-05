# @Time 2022/11/5 11:43
# Author: beijingm

from fastapi import APIRouter, Body, Form, Depends, Path
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestFormStrict, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException

from app.module_route import schema
from .access import UserModelOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:9000/token")
# 主要用来做权限认证
auth = APIRouter()


class Authentication:
    ...


class UserDependencies:

    # 用于验证用户登录的依赖
    @staticmethod
    async def authenticate_user(request: Request, username: str = Form(...),
                                password: str = Form(...)) -> schema.TbUsers:
        sql = schema.select(schema.TbUsers).where(schema.TbUsers.username == username)
        current: schema.TbUsers = await schema.AsyncUserCURD.select_user(sql)
        if not current:
            raise HTTPException(status_code=401, detail={"msg": "用户认证失败，请检查用户名或者密码。"})
        if not current.check_password(password):
            raise HTTPException(status_code=401, detail={"msg": "用户认证失败，请检查用户名或者密码。"})
        _session: dict = {
            "user_id": current.user_id,
            "username": current.username,
            "status": current.status,
            "telephone": current.telephone
        }
        request.session.update(_session)
        return current


@auth.post("/login", response_model=UserModelOut, response_class=ORJSONResponse)
async def login(user: schema.TbUsers = Depends(UserDependencies.authenticate_user)):
    return user


@auth.post("/authenticate")
def authenticate(token: str = Depends(oauth2_scheme)):
    print(token)
    return token


@auth.get("/user/{user_name}")
async def user_me(request: Request, user_name: str = Path(...)):

    if request.session.get("username") == user_name:

        return request.session["user_id"]
