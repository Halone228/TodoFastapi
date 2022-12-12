import time
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response, JSONResponse
from database.pd_models import UserLogin, UserRegister
from database.db_models import User
from .utils import encode_user, JWTBearer
import bcrypt


dep = JWTBearer()


AuthRouter = APIRouter(tags=['Authorization'])


@AuthRouter.post('/registration')
async def registration(user: UserRegister):
    if User.get_or_none(username=user.username) is not None:
        return JSONResponse(status_code=403, content={
            'error': '0',
            'desc': 'User exists!'
            })
    User.create(**user.dict())
    encoded = encode_user(user)
    if encoded is None:
        return Response(status_code=404,content='Something went wrong!\nEnding')
    return {'access_token': encoded}


@AuthRouter.get('/login')
async def login(username: str, password: str):
    if (user := User.get_or_none(username=username)) is None:
        return JSONResponse(status_code=403, content={
            'error': '0',
            'desc': 'User dont exists'
        })
    if user.password != password:
        return JSONResponse(status_code=403, content={
            'error': '1',
            'desc': 'Wrong password'
        })
    return {'access_token': encode_user(UserLogin(username=username, password=password))}
