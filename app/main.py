# 主文件入口

from typing import Union, Optional
import asyncio
import time

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def index():
    await asyncio.sleep(3)
    # time.sleep(3)
    return {"returnCode": 200}


@app.get("/items/{item_id}")
async def item(item_id: int, q: Optional[str] = None):
    return {"item": [{"name": "food"}], "query": q}

