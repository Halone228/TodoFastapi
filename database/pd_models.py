import datetime

from pydantic import BaseModel, validator, ValidationError, EmailStr
from .db_models import User as User_db

_T_id = int | str


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

    @validator('username')
    def validate_username(self, username: str):
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


class UserLogin(BaseModel):
    username: str
    password: str


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
