from fastapi import APIRouter, Depends, Response, Request
from database import pd_models, db_models
from api.auth import dep
from uuid import uuid4

RestRouter = APIRouter()


@RestRouter.get('/get_bg')
async def get_bg(user: pd_models.UserBase = Depends(dep)):
    db_user: db_models.User = db_models.User.get(username=user.username)
    if db_user.bg_image is None:
        return 'image/f0398561-034c-44b3-84a4-dae4c0a743b9'
    return f'image/{str(db_user.bg_image.id)}'

@RestRouter.get('/image/{id}')
async def get_image(**kwargs):
    return Response(content=db_models.ImageStorage.get(**kwargs).bin, media_type='image/jpg')

@RestRouter.post('/save_bg')
async def save_bg(request: Request, user: pd_models.UserBase = Depends(dep)):
    image = db_models.ImageStorage.create(id=str(uuid4()), bin=await request.body)
    user_db: db_models.User = db_models.User.get(username=user.username)
    user_db.bg_image = image
    user_db.save()
