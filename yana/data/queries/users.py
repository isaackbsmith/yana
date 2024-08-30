from yana.data.database import run_query
from yana.data.schemas import NewUserSchema, UserSchema
from yana.domain.types import YANAConfig
from yana.web.logger import logger


async def select_user(config: YANAConfig, user_id: str):
    sql = """
        SELECT
            id,
            first_name,
            last_name,
            email,
            phone_number,
            gender,
            user_type
        FROM users
        WHERE id = :id
    """
    try:
        logger.info("Selecting user")
        return await run_query(config=config,
                                 sql=sql,
                                 params={"id": user_id},
                                 factory=UserSchema,
                                 pragma="one")
    except Exception as e:
        logger.info(f"Error selecting new user: {e}")


async def insert_user(config: YANAConfig, user: NewUserSchema):
    sql = """
        INSERT INTO users (
            id,
            first_name,
            last_name,
            email,
            phone_number,
            password,
            gender,
            user_type,
        ) VALUES (
            :id,
            :first_name,
            :last_name,
            :email,
            :phone_number,
            :password,
            :gender,
            :user_type,
        );
        """
    try:
        logger.info("Inserting new user")
        return await run_query(
            config=config,
            sql=sql,
            params=user.model_dump(),
            factory=NewUserSchema)
    except Exception as e:
        logger.warn(f"Error inserting new user: {e}")


async def update_user(config: YANAConfig, user: UserSchema):
    sql = """
        UPDATE users
        SET
            first_name = :first_name,
            last_name = :last_name,
            email = :email,
            phone_number = :phone_number,
            gender = :gender,
            user_type = :user_type
        WHERE id = :id;
        """
    try:
        logger.info("Updating user")
        return await run_query(
            config=config,
            sql=sql,
            params=user.model_dump(),
            factory=UserSchema)
    except Exception as e:
        logger.warn(f"Error Updating user: {e}")


async def delete_user(config: YANAConfig, user_id: str):
    sql = """
        DELETE FROM users WHERE id = :id;
        """
    try:
        logger.info("Deleting user")
        return await run_query(
            config=config,
            sql=sql,
            params={"id": user_id},
            factory=UserSchema)
    except Exception as e:
        logger.warn(f"Error Deleting user: {e}")
