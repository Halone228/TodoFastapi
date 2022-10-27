import datetime
import time
from enum import Enum

from pydantic import BaseModel, validator, ValidationError, EmailStr, Field
from .db_models import User as User_db
from typing import Optional as optional

_T_id = int | str


class Statuses(str, Enum):
    passive = "passive"
    important = "important"
    in_progress = "in_progress"
    done = "done"
    deadline_close = "deadline_close"
    too_late = "too_late"


class UserBase(BaseModel):
    username: str
    password: str


class UserRegister(UserBase):
    email: EmailStr

    @validator('username')
    def validate_username(cls, username: str):
        username.strip()
        user = User_db.get_or_none(username=username)
        if user is None:
            return username
        else:
            raise ValidationError

    class Config:
        schema_extra = {
            'example': {
                'username': 'user123',
                'password': 'asdasd1234',
                'email': 'example@gmail.com'
            }
        }


class UserLogin(UserBase):
    pass


class ToDoBase(BaseModel):
    title: str
    text: str
    deadline_date: datetime.date
    start_date: datetime.date
    status: Statuses


class ToDo(ToDoBase):
    id: optional[_T_id]
    group: _T_id


class GroupBase(BaseModel):
    group_title: str
    background_color: str
    title_color: str
    text_shadow: bool


class Group(GroupBase):
    id: optional[_T_id]
    todos: list[ToDo] = Field(default=[])


class GroupList(BaseModel):
    values: list[Group]


