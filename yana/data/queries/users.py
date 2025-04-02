from yana.data.database import run_query
from yana.data.schemas.user import NewUserSchema, UserSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.types import YANAConfig


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
        return await run_query(
            config=config,
            sql=sql,
            params={"id": user_id},
            factory=UserSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting new user")


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
            user_type
        ) VALUES (
            :id,
            :first_name,
            :last_name,
            :email,
            :phone_number,
            :password,
            :gender,
            :user_type
        );
        """
    try:
        return await run_query(
            config=config, sql=sql, params=user.model_dump(), factory=UserSchema
        )
    except DatabaseError:
        raise QueryError("Error inserting new user")


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
        return await run_query(
            config=config, sql=sql, params=user.model_dump(), factory=UserSchema
        )
    except DatabaseError:
        raise QueryError("Error updating user")


async def delete_user(config: YANAConfig, user_id: str):
    sql = """
        DELETE FROM users WHERE id = :id;
        """
    try:
        return await run_query(
            config=config, sql=sql, params={"id": user_id}, factory=UserSchema
        )
    except DatabaseError:
        raise QueryError("Error deleting user")
