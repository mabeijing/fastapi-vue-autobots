# 主文件入口

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 处理请求头中`Accept-Ecoding`包含`gzip`的请求
from fastapi.middleware.gzip import GZipMiddleware

from .demo.router import demo
from .demo._requests_base import req_base
from .demo._request_adv import req_adv

import strawberry
# from strawberry.fastapi import GraphQLRouter
from strawberry.asgi import GraphQL

descriptions = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(title='fastapi-vue-autobots',
              description=descriptions, version='v0.0.1')


# @strawberry.type
# class User:
#     name: str
#     age: int

# @strawberry.type
# class Query:
#     @strawberry.field
#     def user(self) -> User:
#         return User(name="Patrick", age=100)

# schema = strawberry.Schema(Query)

# graphql_app = GraphQLRouter(schema)
# graphql_app = GraphQL(schema)

# app.add_route("/graphql", graphql_app)
# app.add_websocket_route("/graphql", graphql_app)
app.include_router(demo)
app.include_router(req_base)
app.include_router(req_adv)

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

# app.add_middleware(GZipMiddleware, niminum_size=1000)

# app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000, workers=1)
