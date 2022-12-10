from fastapi import Depends
from api.auth import dep, JWTBearer
from database import pd_models, db_models
from playhouse.shortcuts import model_to_dict
from fastapi import APIRouter


RestRouter = APIRouter(tags=['Group'])


@RestRouter.get('/get_groups', response_model=pd_models.GroupList)
async def get_group(user: pd_models.UserBase = Depends(dep)) -> pd_models.GroupList:
    groups = db_models\
        .Group\
        .select()\
        .join(db_models.User)\
        .where(db_models.User.username == user.username)
    return pd_models.GroupList(values=[
                        pd_models.Group(**model_to_dict(i)) for i in groups])


@RestRouter.post('/create_group',response_model=pd_models.Group)
async def create_group(group: pd_models.GroupBase, user: pd_models.UserBase = Depends(dep)) -> pd_models.Group:
    created_group = db_models.Group\
        .create(**group.dict(),
                user=db_models.User.get(username=user.username))
    return pd_models.Group(**model_to_dict(created_group, max_depth=0))


@RestRouter.delete('/delete_group/{group_id}')
async def delete_group(group_id: int, user: pd_models.UserBase = Depends(dep)):
    group = db_models.Group.get(id=group_id)
    if group.user.username == user.username:
        group.delete_instance()

@RestRouter.post('/update_group')
async def update_group(newGroup: pd_models.Group, user: pd_models.UserBase = Depends(dep)):
    group = db_models.Group.get(id=newGroup.id)
    if not group.user.username == user.username:
        return Response(status_code=403)
    group = db_models.Group(**newGroup.dict())
    group.save()
