# 工具集

from enum import Enum


class ROUTETag(str, Enum):
    DEMO = "测试"
    USER = "用户"
    ADMIN = "后台"
