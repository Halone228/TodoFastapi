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
    pass

    class Config:
        schema_extra = {
            'example': {
                'username': 'user123',
                'password': 'asdasd1234'
            }
        }


class UserLogin(UserBase):
    pass


class ToDoBase(BaseModel):
    title: str
    text: str
    deadline_date: str#datetime.date
    deadline_time: str#datetime.time
    start_date: str#datetime.date
    start_time: str#datetime.time
    status: str#Statuses
    group: optional[_T_id]

class ToDo(ToDoBase):
    id: optional[_T_id]

class ToDoList(BaseModel):
    todos: list[ToDo]

class GroupBase(BaseModel):
    title: str
    color_scheme: int


class Group(GroupBase):
    id: optional[_T_id]


class GroupList(BaseModel):
    values: list


