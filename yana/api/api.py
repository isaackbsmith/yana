from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from yana.api.exception_handlers import global_exception_handler
from yana.api.middleware import log_requests
from yana.api.routers import adherence, appointments, assistant, users, medications, schedules


# Instantiate app
app = FastAPI(
    title="YANA",
    description="You Are Not Alone",
    version="1.0.0",
)

origins = [
    "http://localhost:5173"
]

# Add middlewares
app.middleware("http")(log_requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exceptions
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/healthcheck")
def root():
    return {"message": "As you can see, I'm not dead!"}

# Add routes
app.include_router(users.router)
app.include_router(medications.router)
app.include_router(appointments.router)
app.include_router(schedules.router)
app.include_router(adherence.router)
app.include_router(assistant.router)

