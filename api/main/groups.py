from fastapi import Depends
from api.auth import dep, JWTBearer
from database import pd_models, db_models
from playhouse.shortcuts import model_to_dict
from fastapi import APIRouter


RestRouter = APIRouter(tags=['Group'])


@RestRouter.get('/groups', response_model=pd_models.GroupList)
async def get_group(user: pd_models.UserBase = Depends(dep)) -> pd_models.GroupList:
    groups = db_models\
        .Group\
        .select()\
        .join(db_models.User)\
        .where(db_models.User.username == user.username)
    print(groups)
    res_list = []
    for group in groups:
        res_group = pd_models.Group(**model_to_dict(group))
        todos = db_models\
            .Todos\
            .select()\
            .join(db_models.Group)\
            .where(db_models.Group.id == group.id)
        res_group.todos = [model_to_dict(i,max_depth=0) for i in todos]
        res_list.append(res_group)
    return pd_models.GroupList(values=res_list)


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
async def update_group(, user: pd_models.UserBase = Depends(dep)):
    group = db_models.Group.get(id=data.id)
    if not group.user.username == user.username:
        return Response(status_code=403)
    group[data.field] = data.value
    group.save()
