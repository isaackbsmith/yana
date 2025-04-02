from fastapi import Request, status
from fastapi.responses import JSONResponse

from yana.domain.exceptions import DatabaseError
from yana.api.exceptions import NotFoundError, ValidationError


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, (NotFoundError, ValidationError)):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    elif isinstance(exc, DatabaseError):
        # Log
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An Internal Server Error Occurred"},
        )
    else:
        # log
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An Unexpected Error Occurred"},
        )
