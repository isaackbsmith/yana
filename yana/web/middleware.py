import http
import time
import logging
from typing import Callable
from fastapi import Request


logger = logging.getLogger(__name__)

async def log_request_middleware(request: Request, call_next: Callable):
    """
    Log all requests and thier processing time
    E.g log: 0.0.0.0:8000 - GET /test 200 OK 1.00ms

    parameters:
        request: Fastapi requet object
        callback: Recieves the request and passes it
        to the corresponding path operation and returns the response

    returns:
        response
    """
    logger.debug("middleware::log_request_middleware")
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)

    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase = ""

    logger.info(f"""{host}:{port} - "{request.method} {url}" {response.status_code} {status_phrase} {formatted_process_time}ms""")

    return response
