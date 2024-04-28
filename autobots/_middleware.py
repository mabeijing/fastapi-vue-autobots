"""
内置中间件
"""

from fastapi import APIRouter

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware



middle = APIRouter()
