# 配置文件

import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES = os.path.join(ROOT_DIR, "app", "admin/templates")

APP = os.path.join(ROOT_DIR, "app")

STATIC: Path = Path(ROOT_DIR).joinpath("app", "static")
IMAGE: Path = Path(STATIC).joinpath("images")
PUBLIC: Path = Path(ROOT_DIR).joinpath("public")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
