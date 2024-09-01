from typing import cast
import uuid
import bcrypt
from yana.data.queries.users import delete_user, insert_user, select_user, update_user
from yana.data.schemas.user import NewUserSchema, UserSchema
from yana.domain.exceptions import QueryError, ServiceError
from yana.domain.models.user import Gender, NewUserModel, UserModel, UserType
from yana.domain.types import YANAConfig
from yana.domain.logger import api_logger


async def fetch_user(config: YANAConfig, user_id: str) -> UserModel | None:
    try:
        result = await select_user(config, user_id)
        if result and isinstance(result, UserSchema):
            user = UserModel(
                id=result.id,
                first_name=result.first_name,
                last_name=result.last_name,
                email=result.email,
                phone_number=result.phone_number,
                gender=Gender.try_from_str(result.gender),
                user_type=UserType.try_from_str(result.user_type)
            )
            return user
        return None
    except QueryError:
        api_logger.error("An error occurred fetching user")
        raise ServiceError("User Service Error")


async def create_user(config: YANAConfig, user: NewUserModel) -> None:

    # hash password
    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Create a UUID
    user_id = str(uuid.uuid4())

    # Create user with id
    new_user = NewUserSchema(
        id = user_id,
        first_name = user.first_name,
        last_name = user.last_name,
        email = str(user.email),
        phone_number = user.phone_number,
        password = hashed_pw.decode("utf-8"),
        gender = user.gender.value,
        user_type = user.user_type.value,
    )

    try:
        await insert_user(config, new_user)
    except QueryError:
        api_logger.error("An error occurred creating user")
        raise ServiceError("User Service Error")


async def modify_user(config: YANAConfig, user: UserModel) -> UserModel:
    updated_user = UserSchema(
        id = user.id,
        first_name = user.first_name,
        last_name = user.last_name,
        email = str(user.email),
        phone_number = user.phone_number,
        gender = user.gender.value,
        user_type = user.user_type.value,
    )

    try:
        await update_user(config, updated_user)
        return cast(UserModel, await fetch_user(config, updated_user.id))
    except QueryError:
        api_logger.error("An error occurred updating user")
        raise ServiceError("User Service Error")


async def remove_user(config: YANAConfig, user_id: str) -> None:
    try:
        await delete_user(config, user_id)
    except QueryError:
        api_logger.error("An error occurred deleting user")
        raise ServiceError("User Service Error")




