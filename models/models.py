import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from constants.roles import Roles
from typing import Optional


class TestUser(BaseModel):
    model_config = ConfigDict(use_enum_values=True)  # 👈 ключевая строка

    email: str = Field(..., description="email")
    fullName: str = Field(..., description="Полное имя")
    password: str = Field(..., description="Пароль")
    passwordRepeat: str = Field(..., description="Пароль же")
    roles: list[Roles] = Field(default=[Roles.USER], description="Роли")
    banned: Optional[bool] = Field(default=None, description="Забанен ли")
    verified: Optional[bool] = Field(default=None, description="Верифицирован ли")

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        """Проверяем, что email должен содержать символ '@'"""
        if '@' not in value:
            raise ValueError("email должен содержать символ '@'")
        return value

    @field_validator("password")
    def check_password(cls, value: str) -> str:
        """Проверяем, что password содержит не менее 8 символов"""
        if len(value) < 8:
            raise ValueError("password должен содержать не менее 8 символов")
        return value

    @model_validator(mode='before')
    def passwords_match(cls, values):
        if values.get('password') != values.get('passwordRepeat'):
            raise ValueError("Пароли не совпадают")
        return values

    # # Добавляем кастомный JSON-сериализатор для Enum
    # class Config:
    #     json_encoders = {
    #         Roles: lambda v: v.value  # Преобразуем Enum в строку
    #     }


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value
