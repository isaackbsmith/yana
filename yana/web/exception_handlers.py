import sys
from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import request_validation_exception_handler as _request_validation_exception_handler
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from yana.web.logger import logger


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Wrapper for the default RequestValidation handler of FastAPI that is
    called when client input is invalid
    """
    logger.debug("Custom request_validation_exception_handler was called")
    body  = await request.body()
    query_params = request.query_params._dict
    detail = {"errors": exc.errors(), "body": body.decode(), "query_params": query_params}
    logger.info(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse | Response:
    """
    Wrapper for the default HTTPException handler of FastAPI that is
    called when an HTTPException is explicitly raised
    """
    logger.debug("Custom http_exception_handler was called")
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    Log all unhandled exceptions
    """
    logger.debug("Custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exc_type, exc_value, exc_traceback = sys.exc_info()
    exc_name = getattr(exc_type, "__name__", None)
    logger.error(f"""{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exc_name}: {exc_value}>""")
    return PlainTextResponse(str(exc), status_code=500)
