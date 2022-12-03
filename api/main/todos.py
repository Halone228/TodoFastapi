from fastapi import Depends, Request, Response, Body
from api.auth import dep, JWTBearer
from database import pd_models, db_models
from playhouse.shortcuts import model_to_dict
from fastapi import APIRouter


RestRouter = APIRouter(tags=['Todo'])


@RestRouter.post('/create_todo/{group_id}', response_model=pd_models.ToDo)
async def create_todo(group_id: int,
                       todo: pd_models.ToDoBase,
                       user: JWTBearer = Depends(dep)):
    created = db_models.Todos.create(**todo.dict(),
                                     group=db_models.Group.get(id=group_id))
    return pd_models.ToDo(**model_to_dict(created, max_depth=0))


@RestRouter.post('/update')
async def update_status(todo_new: pd_models.ToDo, user: JWTBearer = Depends(dep)):
    todo = db_models.Todos(**todo_new.dict())
    if todo.user.username != user.username:
        return Response(status_code=403)
    todo.save()


@RestRouter.delete('/delete_todo/{todo_id}')
async def delete_todo(todo_id: int, user: pd_models.UserBase = Depends(dep)):
    todo = db_models.Todos.get(id=todo_id)
    if todo.group.user.username == user.username:
        todo.delete_instance()
