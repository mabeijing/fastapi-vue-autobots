from fastapi import APIRouter, Path, Body, Query
from pydantic import BaseModel, EmailStr, Field

req_adv = APIRouter()


class UserModel(BaseModel):
    id: int = Field(..., title="用户ID", description="用户id")
    name: str
    email: EmailStr


@req_adv.post("/register/{user_id}")
def user(
        user_id: int = Path(title='USER_ID'),
        user: UserModel = Body(...),
        q: bool = Query(default=False, alias="item-query")
):
    """
    1. 支持别名参数 item-query, 由于python不支持-,使用alias
    2. 可以用Path, Body, Query指定更多细节。
    """
    return {"user_id": user_id, "user": user, "q": q}
