from fastapi import Depends, Request, Response, Body
from api.auth import dep, JWTBearer
from database import pd_models, db_models
from playhouse.shortcuts import model_to_dict
from fastapi import APIRouter


RestRouter = APIRouter(tags=['Todo'])


@RestRouter.get('/get_group_todo/{group_id}')
async def get_todo(group_id: int,
                    user: pd_models.UserBase = Depends(dep)) -> pd_models.ToDoList:
    group = db_models.Group.get(id=group_id)
    if not group.user.username == user.username:
        return Response(status_code=403)
    return pd_models.ToDoList(
        todos=[
            model_to_dict(todo, max_depth=0) for todo in
                db_models.Todos.select()\
                .join(db_models.Group)\
                .where(db_models.Group.id==group_id)]
    )


@RestRouter.post('/create_todo/{group_id}', response_model=pd_models.ToDo)
async def create_todo(group_id: int,
                       todo: pd_models.ToDoBase,
                       user: JWTBearer = Depends(dep)):
    created = db_models.Todos.create(**todo.dict(),
                                     group=db_models.Group.get(id=group_id))
    return pd_models.ToDo(**model_to_dict(created, max_depth=0))


@RestRouter.post('/update_todo')
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
