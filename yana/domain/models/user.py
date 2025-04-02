from enum import Enum
from typing import Self
from pydantic import BaseModel, EmailStr


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for gender in cls:
            if gender.value == value.lower():
                return gender
        raise ValueError(f"{value} must be a valid gender")


class UserType(str, Enum):
    PRIMARY = "primary"
    AUXILIARY = "auxiliary"
    PROFESSIONAL = "Professional"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for user_type in cls:
            if user_type.value == value.lower():
                return user_type
        raise ValueError(f"{value} must be a valid user type")


class BaseUserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    gender: Gender
    user_type: UserType


class UserModel(BaseUserModel):
    id: str


class NewUserModel(BaseUserModel):
    password: str
