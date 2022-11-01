# @Time 2022/10/26 19:22
# Author: beijingm

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# pool_size=10 表示连接池最多常驻10个conn，
# max_overflow=15 允许最大的并发数为15，但是有5个conn用完后会关闭，而不是放回连接池。
# pool_timeout=30 默认30秒，如果15个连接已经沾满，新来的连接等待15秒就放弃了。
# pool_recycle=-1 表示连接池永不过期，3600表示一个小时过期，但是如果超过mysql的过期时间，依然会过期。
# poolclass 默认时QueuePool连接池，如果指定NullPool，表示禁用连接池。启动连接池后，session.close()也不能真正关闭connect。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    pool_size=10,max_overflow=15, pool_timeout=30, pool_recycle=-1, poolclass=QueuePool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


