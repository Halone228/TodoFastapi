import time

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from config import JWT_ALGORITHM,SECRET
from jwt import encode as encode_, decode as decode_
from database.pd_models import UserLogin, UserRegister
from database.db_models import User


def encode(data: dict):
    if data.get('expires') is None:
        return None
    return encode_(data, SECRET, algorithm=JWT_ALGORITHM)


def decode(token: str):
    decoded = decode_(token, SECRET, algorithms=JWT_ALGORITHM)
    if decoded.get('expires') <= time.time():
        return None
    return decoded


router = APIRouter()


@router.post('/registration')
async def registration(user: UserRegister, request: Request):
    User.create(**user.dict())
    encoded = encode({
        'expires': time.time() + (60*60*24*15),
        'username': user.username,
        'password': user.password
    })
    if encoded is None:
        return Response(status_code=404,content='Something went wrong!\nEnding')
    request.headers['Authorization'] = 'Bearer '+encoded
    return {'access_token': encoded}
