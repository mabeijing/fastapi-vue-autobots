# @Time 2022/11/5 14:37
# Author: beijingm

from typing import Optional

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from passlib.exc import UnknownHashError
from fastapi.exceptions import RequestValidationError, ValidationError


def default_error_handle(request, exc):
    return ORJSONResponse(content={"errors": str(exc)}, status_code=422)


def un_know_hash_error_handle(request, exc):
    if isinstance(exc, UnknownHashError):
        return ORJSONResponse(content={"errors": exc.message}, status_code=422)
    for error in exc.errors():
        error: dict
        error["loc"] = '->'.join(error["loc"])
    return ORJSONResponse(content={"errors": exc.errors()}, status_code=422)


def request_validation_error_handle(request, exc):
    if isinstance(exc, RequestValidationError):
        for error in exc.errors():
            error: dict
            error["loc"] = '->'.join(error["loc"])
        return ORJSONResponse(content={"errors": exc.errors()}, status_code=422)


def validation_error_handle(request, exc):
    if isinstance(exc, ValidationError):
        for error in exc.errors():
            error: dict
            error["loc"] = '->'.join(error["loc"])
        return ORJSONResponse(content={"errors": exc.errors()}, status_code=422)


class ExceptionHandles:

    def __init__(self, app: FastAPI = None):
        self.app: Optional[FastAPI] = app
        if self.app:
            self.handler_function()

    def init_app(self, app: FastAPI):
        self.app: FastAPI = app
        self.handler_function()

    def handler_function(self):
        self.app.add_exception_handler(UnknownHashError, un_know_hash_error_handle)
        self.app.add_exception_handler(RequestValidationError, request_validation_error_handle)
        self.app.add_exception_handler(ValidationError,validation_error_handle)
        self.app.add_exception_handler(Exception, default_error_handle)
