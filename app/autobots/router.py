# 模块路由文件

from enum import Enum
from typing import Optional, Set, TYPE_CHECKING
from datetime import datetime, date, time
from decimal import Decimal
from urllib import request
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from fastapi import APIRouter, Body, Path, Request, params, Response, Depends, WebSocket

# from fastapi.responses import JSONResponse   json是python实现的json解析，性能不高。
# from fastapi.responses import UJSONResponse  ujson是c实现的高性能json解析，但是解析有边缘影响。
# from fastapi.responses import ORJSONResponse  orjson是rust实现的高性能json，目前没啥问题。
# from fastapi.responses import HTMLResponse    用于返回html
# from fastapi.responses import PlainTextResponse   用于返回纯文本或者字节
# from fastapi.responses import RedirectResponse    用于重定向路由
# from fastapi.responses import StreamingResponse   用于异步生成器/迭代器，流式传输响应主体。注意，这个插件也可以异步读取文件，异步读取文件库aiofile
# from fastapi.responses import FileResponse  这个支持异步传输文件作为响应
from fastapi.templating import Jinja2Templates    # 需要安装jinja2, 配合HTMLResponse使用

from starlette.responses import JSONResponse
from fastapi.responses import ORJSONResponse, HTMLResponse

templates = Jinja2Templates(directory="templates")


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


@demo.post("/order/{order_id:path}", response_class=ORJSONResponse)
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

    return HTMLResponse(content="ORJSONResponse", status_code=404, media_type="text/html")


@demo.get("/home")
def home(request: Request):
    templates.TemplateResponse("home.html", {"request": request})


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


def welcome():
    """
    返回html内容
    """
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


demo.get("/", response_class=HTMLResponse)(welcome)

@demo.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            print(q)
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@demo.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}



