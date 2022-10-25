import datetime

from pydantic import BaseModel, validator, ValidationError
from .db_models import User as User_db

_T_id = int | str


class User(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(self, username: str):
        username.strip()
        user = User_db.get_or_none(username=username)
        if user is None:
            return username
        else:
            raise ValidationError


class Group(BaseModel):
    id: optional[_T_id]
    group_title: str
    background_color: str
    title_color: str
    text_shadow: str


class ToDo(BaseModel):
    id: optional[_T_id]
    title: str
    text: str
    deadline_date: datetime.date
    status: str
    group_id: _T_id
