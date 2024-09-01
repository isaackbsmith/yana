from fastapi import FastAPI

from yana.web.exception_handlers import global_exception_handler
from yana.web.middleware import log_requests
from yana.web.routers import users, medications, schedules


# Instantiate app
app = FastAPI(
    title="YANA",
    description="You Are Not Alone",
    version="1.0.0",
    redoc_url="/",
)

# Add middleware
app.middleware("http")(log_requests)

# Add exceptions
app.add_exception_handler(Exception, global_exception_handler)

# Add routes
app.include_router(users.router)
app.include_router(medications.router)
app.include_router(schedules.router)
