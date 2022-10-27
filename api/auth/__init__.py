import time
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from database.pd_models import UserLogin, UserRegister
from database.db_models import User
from .utils import encode_user, JWTBearer


dep = JWTBearer()


AuthRouter = APIRouter(tags=['Authorization'])


@AuthRouter.post('/registration')
async def registration(user: UserRegister):
    if User.get_or_none(username=user.username) is not None:
        return Response(status_code=402, content='User with that username exists')
    User.create(**user.dict())
    encoded = encode_user(user)
    if encoded is None:
        return Response(status_code=404,content='Something went wrong!\nEnding')
    return {'access_token': encoded}


@AuthRouter.post('/login')
async def login(user: UserLogin):
    if User.get_or_none(username=user.username,password=user.password) is None:
        return Response(status_code=403, content='No such user')
    return {'access_token': encode_user(user)}
