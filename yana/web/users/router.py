from fastapi import APIRouter
from fastapi.exceptions import HTTPException


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
async def home() -> str:
    raise HTTPException(status_code=400, detail="No")

