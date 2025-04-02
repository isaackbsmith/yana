from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.user import BaseUserModel, NewUserModel, UserModel
from yana.service.users import create_user, fetch_user, modify_user, remove_user
from yana.api.exceptions import InternalServerError
from yana.api.types import Config


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="This endpoint is not allowed"
    )


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def new_user(config: Config, user: NewUserModel):
    try:
        return await create_user(config, user)
    except ServiceError:
        raise InternalServerError


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user(config: Config, user_id: str):
    try:
        user = await fetch_user(config, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
        return user
    except ServiceError:
        raise InternalServerError


@router.put("/{user_id}", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def update_user(config: Config, user_id: str, user: BaseUserModel):
    try:
        p_user = await fetch_user(config, user_id)
        if not p_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User does not exist",
            )
        return await modify_user(config, user, user_id)
    except ServiceError:
        raise InternalServerError


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(config: Config, user_id: str):
    try:
        user = await fetch_user(config, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
        await remove_user(config, user_id)
        return {"message": "User deleted successfully"}
    except ServiceError:
        raise InternalServerError
