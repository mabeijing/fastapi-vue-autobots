# 主文件入口
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 处理请求头中`Accept-Encoding`包含`gzip`的请求
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette_session import SessionMiddleware
from starlette_session.backends import BackendType

from autobots import settings
from autobots.views import route, access, socket, auth
from autobots.exceptions import ExceptionHandles

# patch.patch_all()

descriptions = """
App API helps you do awesome stuff. 🚀
"""

redis_client = redis.Redis(host="127.0.0.1", password="root@123")
app = FastAPI(title='fastapi-vue-autobots', description=descriptions, version='v0.0.1')
exception = ExceptionHandles()
exception.init_app(app)

app.state.template = Jinja2Templates(directory=settings.TEMPLATES)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    cookie_name="cookie",
    max_age=3600,
    backend_type=BackendType.redis,
    backend_client=redis_client
)

# app.add_middleware(HTTPSRedirectMiddleware)

# app.add_middleware(TrustedHostMiddleware,
#                    allowed_hosts=["example.com", "*.example.com"])

app.add_middleware(GZipMiddleware, minimum_size=1000)

# app.mount可以挂在多个静态目录。
# 第一个位置参数：路由。 http://localhost:8000/static
# 第二个是挂在的实际路径，是脚本执行的目录作为相对目录。区别win和mac，最好的就是通过settings定位到根目录

app.mount("/static", StaticFiles(directory=settings.STATIC), name="static")
app.mount("/public", StaticFiles(directory=settings.PUBLIC), name="pub")

app.include_router(route)
app.include_router(access)
app.include_router(socket)
app.include_router(auth)

