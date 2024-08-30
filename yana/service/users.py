import uuid
import bcrypt
from yana.data.queries.users import delete_user, insert_user, select_user, update_user
from yana.data.schemas import NewUserSchema, UserSchema
from yana.domain.models import Gender, NewUserModel, UserModel, UserType
from yana.domain.types import YANAConfig
from yana.web.logger import logger


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
    except Exception as e:
        logger.warn(f"An error occurred fetching user: {e}")
        raise


async def create_user(config: YANAConfig, user: NewUserModel) -> None:
    logger.info("Service: Creating new user")

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
    except Exception as e:
        logger.info(f"An error occured: {e}")
        raise


async def modify_user(config: YANAConfig, user: UserModel) -> UserModel | None:
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
        return await fetch_user(config, updated_user.id)
    except Exception as e:
        logger.info(f"An error occured: {e}")
        raise


async def remove_user(config: YANAConfig, user_id: str) -> None:
    try:
        await delete_user(config, user_id)
    except Exception as e:
        logger.info(f"An error occured: {e}")
        raise




