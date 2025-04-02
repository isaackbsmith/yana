from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    gender: str
    user_type: str


class NewUserSchema(UserSchema):
    password: str
