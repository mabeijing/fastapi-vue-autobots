# 主文件入口

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .admin.router import admin


app = FastAPI()


app.include_router(admin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000, workers=1)
