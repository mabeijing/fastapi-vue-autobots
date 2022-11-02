# 主文件入口
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 处理请求头中`Accept-Encoding`包含`gzip`的请求
from fastapi.middleware.gzip import GZipMiddleware

from app.module_route import route, access

from app import settings

descriptions = """
App API helps you do awesome stuff. 🚀
"""

app = FastAPI(title='fastapi-vue-autobots', description=descriptions, version='v0.0.1')

app.state.template = Jinja2Templates(directory=settings.TEMPLATES)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.add_middleware(HTTPSRedirectMiddleware)

# app.add_middleware(TrustedHostMiddleware,
#                    allowed_hosts=["example.com", "*.example.com"])

app.add_middleware(GZipMiddleware, minimum_size=1000)

# app.mount可以挂在多个静态目录。
# 第一个位置参数：路由。 http://localhost:8000/static
# 第二个是挂在的实际路径，是脚本执行的目录作为相对目录。区别win和mac，最好的就是通过settings定位到根目录
# 第三个参数name，尚未搞清楚。

app.mount("/static", StaticFiles(directory=settings.STATIC), name="static")
app.mount("/public", StaticFiles(directory=settings.PUBLIC), name="pub")

app.include_router(route)
app.include_router(access)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="app.main:app", host="127.0.0.1", port=8000, reload=True, debug=True)
