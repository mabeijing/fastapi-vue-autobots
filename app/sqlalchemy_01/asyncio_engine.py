# @Time 2022/10/26 20:50
# Author: beijingm

import asyncio

from sqlalchemy.ext.asyncio import  create_async_engine



engine = create_async_engine("postgresql+asyncpg://scott:tiger@localhost/test", echo=True)


