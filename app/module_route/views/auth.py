# @Time 2022/11/5 11:43
# Author: beijingm
from typing import Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Form, Depends, Path
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt

from app.module_route import schema
from app.module_route.views.access import UserModelOut
from app import settings

# 主要用来做权限认证
auth = APIRouter(prefix="/auth")

# 验证header下的Authentication字段
# 这里，tokenUrl是可以指向其他网站做单点登录的。只要能返回token即可
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class UserDependencies:

    # 用户验证器
    @staticmethod
    async def authenticate(username: str, password: str) -> schema.TbUsers:
        sql = schema.select(schema.TbUsers).where(schema.TbUsers.username == username)
        current: schema.TbUsers = await schema.AsyncUserCURD.select_user(sql)
        if not current:
            raise HTTPException(status_code=401, detail={"msg": "用户认证失败，请检查用户名或者密码。"})
        if not current.check_password(password):
            raise HTTPException(status_code=401, detail={"msg": "用户认证失败，请检查用户名或者密码。"})
        return current

    # 用于验证用户登录Form的依赖
    @staticmethod
    async def authenticate_user_form(request: Request, username: str = Form(...),
                                     password: str = Form(...)) -> schema.TbUsers:
        current: schema.TbUsers = await UserDependencies.authenticate(username=username, password=password)

        _session: dict = {
            "user_id": current.user_id,
            "username": current.username,
            "status": current.status,
            "telephone": current.telephone
        }
        request.session.update(_session)
        return current

    @staticmethod
    async def get_user(request: Request, username: str = Path(..., example="Ada Wang")) -> schema.TbUsers:
        sql = schema.select(schema.TbUsers).where(schema.TbUsers.username == username)
        current: schema.TbUsers = await schema.AsyncUserCURD.select_user(sql)
        if not current:
            raise HTTPException(status_code=405, detail={"msg": "查询用户不存在。"})

        return current


class JwtUtils:

    @staticmethod
    def _jwt_encode(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode: dict = data.copy()
        if expires_delta:
            expire: datetime = datetime.utcnow() + expires_delta
        else:
            expire: datetime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def generate_token(request: Request, form: OAuth2PasswordRequestForm = Depends()) -> dict:
        user: schema.TbUsers = await UserDependencies.authenticate(username=form.username, password=form.password)
        payload: dict = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "telephone": user.telephone,
            "status": user.status
        }
        request.session.update({"user_id": payload})
        token: str = JwtUtils._jwt_encode(payload)
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    def authenticate_token(token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload: dict = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except JWTError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return payload


@auth.post("/login", response_model=UserModelOut, response_class=ORJSONResponse)
async def login(user: schema.TbUsers = Depends(UserDependencies.authenticate_user_form)) -> UserModelOut:
    return user


@auth.get("/user/{username}", response_model=UserModelOut, dependencies=[Depends(JwtUtils.authenticate_token)])
async def user_me(user: schema.TbUsers = Depends(UserDependencies.get_user)):
    return user


@auth.post("/token")
async def login(token: dict = Depends(JwtUtils.generate_token)) -> dict:
    return token
