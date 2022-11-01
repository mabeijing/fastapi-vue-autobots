# 配置文件

import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES = os.path.join(ROOT_DIR, "app", "templates")

APP = os.path.join(ROOT_DIR, "app")

STATIC: Path = Path(ROOT_DIR).joinpath("app", "static")
IMAGE: Path = Path(STATIC).joinpath("images")
PUBLIC: Path = Path(ROOT_DIR).joinpath("public")
