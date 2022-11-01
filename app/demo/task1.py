# @Time 2022/10/27 14:13
# Author: beijingm

"""

1. dev2 测试 postgres 在1亿数据量下的性能表现，
2. 测试环境： postgres 节点 8G内存，CPU资源无限制。
3. 测试场景
    1. 10亿条数据，单次请求41000条（NXS）。
    2. 10亿条数据，单次请求1亿条，（模拟）



"""
import asyncio

import httpx

from typing import Optional, Any
from pydantic import BaseModel, Field


def to_bool(d: Any) -> bool:
    if d == "none":
        return False
    return bool(d)


class VersionModel(BaseModel):
    productID: Optional[int]
    versionID: int
    rmID: int
    type: int
    versionName: str
    gaDate: str
    codename: str = ""
    description: str
    projectRegistered: bool = Optional[bool]


class ProjectModel(BaseModel):
    productName: str
    alias: str = ""
    officialName: str
    description: str
    productID: int
    status: int
    versions: list[VersionModel]
    businessUnit: dict
    projectRegistered: Optional[bool] = False
    productRegistered: Optional[bool] = Field(None)


session = httpx.AsyncClient()

url = 'http://10.148.61.2:18090/api/gabidategw/searchnoregistproduct'
body = {"page": 1, "pageSize": 20, "productID": "", "productName": "", "statuses": []}
headers = {"session": "a0d77938d2bf180c0e46d714a4cd3868"}

data: list[ProjectModel] = []


async def main():
    response = await session.post(url, json=body, headers=headers)
    rows: list[dict] = response.json()["products"]["rows"]
    for row in rows:
        try:
            project = ProjectModel(**row)
        except Exception as e:
            print(e)
        else:
            if project.versions:
                data.append(project)


if __name__ == '__main__':
    import time

    t1 = time.time()
    loop = asyncio.get_event_loop()
    tasks = [main() for i in range(1)]
    loop.run_until_complete(asyncio.wait(tasks))
    print(f"cost {time.time() - t1}")
    # print(data)

    for d in data:
        print(d.productName)
        print(d.productID)
        # print(d.productRegistered)
        print(d.versions)
        print('--------------')
