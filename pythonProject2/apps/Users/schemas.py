from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from apps.Users.schema_validation import username_validation, password_validation


class UserRegistrationRequestSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    user_name: str
    password: str
    email: EmailStr

    # validators
    @field_validator('user_name')
    def username_validation_option(cls, value):
        return username_validation(username=value)

    @field_validator('password')
    def password_validation_option(cls, value):
        return password_validation(password=value)


class UserLoginRequestSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    user_name: str
    password: str

    # validators
    @field_validator('user_name')
    def username_validation_option(cls, value):
        return username_validation(username=value)


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    user_name: str
    email: str
