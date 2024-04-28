# @Time 2022/11/4 23:32
# Author: beijingm


from fastapi import exceptions
from pydantic import create_model, BaseConfig
from pydantic import error_wrappers
from pydantic.errors import MissingError, EmailError


def patch_all():
    error_wrappers._EXC_TYPE_CACHE = {
        MissingError: "value_error.missing",
        EmailError: "邮件错误类"
    }

    class Config(BaseConfig):

        # allow_population_by_field_name = True
        error_msg_templates = {
            "value_error.missing": "必填字段缺失",
            "邮件错误类": "非法邮箱格式",
            "value_error.number.not_gt": "确保值必须大于{limit_value}"
        }

    exceptions.RequestErrorModel = create_model("RequestModel", __config__=Config)
    exceptions.WebSocketErrorModel = create_model("WebSocket", __config__=Config)
