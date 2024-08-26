from fastapi import APIRouter
from fastapi.exceptions import HTTPException


router = APIRouter(
    prefix="/adherence",
    tags=["adherence"]
)


@router.get("/")
async def home() -> str:
    return "Hello"

