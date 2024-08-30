from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.models import NewUserModel, UserModel
from yana.service.users import create_user, fetch_user
from yana.web.types import Config


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
async def home() -> str:
    raise HTTPException(status_code=400, detail="No")


@router.post("/new", response_model=dict, status_code=status.HTTP_201_CREATED)
async def new_user(config: Config, user: NewUserModel):
    try:
        await create_user(config, user)
        return {"message": "User created successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create user")


@router.get("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user(config: Config, user_id: str):
    try:
        user = await fetch_user(config, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        return user
    except Exception as e:
        print(e)


@router.put("/{user_id}", response_model=UserModel)
async def update_user(config: Config, user_id: str, user: UserModel):
    try:
        user = await fetch_user()






