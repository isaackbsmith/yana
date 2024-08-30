from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from yana.web.dependencies import get_config
from yana.web.middleware import log_request_middleware
from yana.web.exception_handlers import (
        request_validation_exception_handler,
        http_exception_handler,
        unhandled_exception_handler
)
from yana.web.routers import users


app = FastAPI(
    title="YANA",
    description="You Are Not Alone",
    version="1.0.0",
    redoc_url="/",
)


# Add middleware
app.middleware("http")(log_request_middleware)

# Add exceptions
# app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
# app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Add routes
app.include_router(users.router)
