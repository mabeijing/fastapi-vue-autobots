# @Time 2022/11/1 13:22
# Author: beijingm

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import PlainTextResponse, HTMLResponse, ORJSONResponse, FileResponse, StreamingResponse
from fastapi.requests import Request

import logging
from uuid import uuid4
import aiofiles
from app import settings
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates
from app.utils import ROUTETag
import datetime

route = APIRouter(prefix="/route")

logger = logging.getLogger()


@route.get("/hello-world", description='你好世界', name='hello world', tags=[ROUTETag.DEMO],
           response_description='字节文本', response_class=PlainTextResponse, response_model=bytes)
def route_list():
    """
    PlainTextResponse 字节响应
    """
    content: bytes = b"hello world!"
    return PlainTextResponse(content=content, status_code=200)


@route.get("/welcome", description="首页", name="welcome", tags=[ROUTETag.ADMIN], response_description="html响应",
           response_class=HTMLResponse)
def route_list(request: Request):
    """
    支持Jinja2的模板语法。
    可以通过request.app.state.template拿到app.state.template = Jinja2Template()的值。
    {"request":request}是必填项。
    """
    template: Jinja2Templates = request.app.state.template
    return template.TemplateResponse("welcome.html", context={"request": request, "information": "welcome!"})


@route.get("/home", tags=[ROUTETag.ADMIN], response_description="json响应", response_class=ORJSONResponse)
def home():
    """
    orjson 性能很高，并且支持python基本数据类型，datetime，time，数据类，Enum, UUID，挺好的
    """

    data = [{
        "id": uuid4(),
        "name": "beijingm",
        "bod": {
            "na": ["12", 23, datetime.datetime.now()],
            "use": ROUTETag.ADMIN
        }
    }]
    return ORJSONResponse(content=data)


@route.post("/avatar", tags=[ROUTETag.ADMIN], response_description="头像上传(小)", response_class=PlainTextResponse)
async def readfile(image: bytes = File(...)):
    """
    图片文件二进制流写入本地文件。因为会用内存接收文件字节流，所以不能传大文件。
    如果是小于10k，则可以使用str = base64.b64encode(bytes)将字节流转化成字符串。通过byte = base64.b64decode(str)读取写入文件。
    """
    # byte / 1024 = kb
    if len(image) / 1024 > 800:
        return PlainTextResponse("文件内容大于800kb，请检查!")
    image_name = settings.IMAGE.joinpath(f"{str(uuid4())}.png")
    async with aiofiles.open(image_name, mode='wb') as f:
        await f.write(image)

    return PlainTextResponse(str(image_name.relative_to(settings.APP)))


class UploadsModel(BaseModel):
    filename: str
    filetype: str


@route.post("/uploads", tags=[ROUTETag.ADMIN],
            response_description="批量上传大文件", response_model=list[UploadsModel])
async def uploads(files: list[UploadFile] = File(...)):
    """
    UploadFile是一个类，包含了filename，content_type，以及一个异步file.read()
    """
    response = []
    for file in files:
        f = await file.read()
        async with aiofiles.open(settings.PUBLIC.joinpath(file.filename), mode='wb') as fd:
            await fd.write(f)
        tmp = {
            "filename": file.filename,
            "filetype": file.content_type
        }
        response.append(tmp)
    return response


@route.get("/download/{file}", tags=[ROUTETag.ADMIN], response_description="上传指定文件",
           response_class=FileResponse)
async def download(file: str):
    """
    FileResponse是异步传输文件作为响应
    支持自定文件类型，响应头。
    关键是如果给出filename，就会产生下载效果，如果不指定，则直接显示。
    """
    return FileResponse(path=settings.IMAGE.joinpath(file), filename='abc.png')


def fake_video_streamer():
    with open(settings.PUBLIC.joinpath("big_buck_bunny.mp4"), mode='rb', buffering=10240) as f:
        yield from f


@route.get("/video", tags=[ROUTETag.ADMIN], response_description="视频播放", response_class=StreamingResponse)
async def video():
    """
    如果不加媒体类型，可能无法播放
    这里仅仅做展示，真的流媒体，需要ffmeg来做了
    """
    return StreamingResponse(fake_video_streamer(), media_type='video/mp4')
