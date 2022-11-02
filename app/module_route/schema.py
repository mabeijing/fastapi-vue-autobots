from sqlalchemy import Column, Integer, String, create_engine, Boolean, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, Session, sessionmaker, scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine.result import ChunkedIteratorResult
from typing import Union

# engine = create_engine("mysql+pymysql://root:Root123!@localhost/tms")
# Base = declarative_base(bind=engine)
# s = sessionmaker(bind=engine)

async_engine = create_async_engine("mysql+aiomysql://root:Root123!@localhost/tms")
Base = declarative_base(bind=async_engine)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

"""
Column()参数详解：
name 可以是第一个位置参数，也可以是任意的name=""
type_ 可是第二个位置参数，也可以是任意的type_=""
autoincrement 为没有外键依赖项的整数主键配置自增长。对于id主键默认使用，对于复合主键
default 默认值。
doc 文档。不会出现在sql中
key ？
index。 字段创建索引， Index("ix_some_table_x", "x")
同时配置unique=True, index=True，默认产生创建唯一索引DDL。而不是创建索引的效果。
info 可选字段，内容填充到schemaitem中。
nullable=False， 不可为None
onupdate UPDATE语句会执行该值。
primary_key 将字段设置为主键，可以设置多个字段组成复合主键
server_default = text('NOW()') => timestamp DATETIME DEFAULT NOW()
unique=True 唯一约束
comment。备注

SQLAlchemy常用数据类型：
1、Integer：整形，映射到数据库中是int类型
2、Float：浮点类型，映射到数据库中是float类型。它占据的32位
3、Double：双精度浮点类型，映射到数据库中是double类型，占据64位
4、String：可变字符类型，映射到数据库中是varchar类型
5、Boolean：布尔类型，映射到数据库中是tinyint类型
6、Decimal：定点类型，是专门为了解决浮点类型精度丢失的问题的，一般作用于金钱类型
7、Enum：枚举类型，指定某个字段只能是枚举中指定的几个值，不能为其他值
8、Date：存储时间，只能存储年月日，映射到数据库中是date类型
9、Datetime：存储时间，可以存储年月日时分秒
10、Time：存储时间，存储时分秒
11、Text：存储长字符串，映射到数据库是text类型
12、Longtext：长文本类型，映射到数据库中是longtext类型
"""


class TbUsers(Base):
    __tablename__ = "tb_user"
    id = Column("ID", Integer, primary_key=True, nullable=False, autoincrement=True, comment="主键ID")
    username = Column("USERNAME", String(50), nullable=False, unique=True, index=True, comment="用户名")
    password = Column("PASSWORD", String(200), nullable=False, comment="用户密码")
    user_id = Column("USERID", Integer, nullable=False, unique=True, index=True, comment="用户ID")
    custom_id = Column("CUSTOM_ID", Integer, nullable=False, unique=True, index=True, comment="客户ID")

    nickname = Column("NICKNAME", String(128), comment="用户昵称")
    avatar = Column("AVATAR", String(128), comment="用户头像")
    telephone = Column("TELEPHONE", String(18), nullable=False, unique=True, comment="手机号")
    email = Column("EMAIL", String(50), nullable=False, unique=True, comment="电子邮件")
    status = Column("STATUS", Integer, default=0, comment="用户状态")
    role = Column("ROLE", Integer, default=1, comment="用户角色")

    province = Column("PROVINCE", String(50), comment="省份")
    city = Column("CITY", String(50), comment="城市")
    county = Column("COUNTY", String(50), comment="区县")
    address = Column("ADDRESS", String(200), comment="具体地址")
    address_detail = column_property(province + city + county + address)

    delete = Column("DELETE", Boolean, default=False, comment="逻辑删除")
    creator = Column("CREATOR", String(30), comment="创建人")
    create_time = Column("CREATE_TIME", DateTime, default=datetime.now, comment="创建时间")
    update_by = Column("UPDATE_BY", String(32), comment="更新人")
    update_time = Column("UPDATE_TIME", DateTime, onupdate=datetime.now, comment="更新时间")
    delete_by = Column("DELETE_BY", String(32), comment="删除人")
    delete_time = Column("DELETE_TIME", DateTime, comment="删除时间")


class AsyncUserCURD:
    TbUsers = TbUsers

    @staticmethod
    async def add_user(user):
        async with async_session() as session:
            session: AsyncSession
            async with session.begin():
                session.add(user)
            await session.commit()

    @staticmethod
    async def select_user():
        async with async_session() as session:
            sql = select(TbUsers).where(TbUsers.username == "beijingm")
            result: ChunkedIteratorResult = await session.execute(sql)
            user: TbUsers = result.scalars().first()
            print(user)

    @staticmethod
    async def update_user():
        async with async_session() as session:
            session: AsyncSession
            sql = update(TbUsers).where(TbUsers.username == "beijingm").values({TbUsers.nickname: "帅帅"})
            async with session.begin():
                await session.execute(sql)

    @staticmethod
    async def delete_user():
        async with async_session() as session:
            session: AsyncSession
            sql = delete(TbUsers).where(TbUsers.username == "zhangsan")
            async with session.begin():
                await session.execute(sql)


if __name__ == '__main__':
    import asyncio


    # 异步创建表
    async def create_all():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await async_engine.dispose()


    user = TbUsers(username="zhangsan", password="root@123", user_id=100100101, custom_id=101, nickname="二狗",
                   telephone="18651815401", email="68149278@qq.com")

    asyncio.run(AsyncUserCURD.add_user(user))
    asyncio.run(AsyncUserCURD.update_user())
    asyncio.run(AsyncUserCURD.delete_user())
    asyncio.run(AsyncUserCURD.select_user())
