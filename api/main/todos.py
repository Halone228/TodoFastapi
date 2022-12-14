from fastapi import Depends, Request, Response, Body
from api.auth import dep, JWTBearer
from database import pd_models, db_models
from playhouse.shortcuts import model_to_dict
from fastapi import APIRouter


RestRouter = APIRouter(tags=['Todo'])


delimiter = '-'


@RestRouter.get('/get_todos/{groups_id}')
#-
async def get_todo(groups_id: str,
                    user: pd_models.UserBase = Depends(dep)):
    ids = [int(i) for i in groups_id.split(delimiter) if i.isdigit()]
    todos = []
    for i in ids:
        group = db_models.Group.get(id=i)
        # if not group.user.username == user.username:
        #     return Response(status_code=403)
        todos += [
            model_to_dict(todo, max_depth=0)  for todo in
                db_models.Todos.select()\
                .join(db_models.Group)\
                .where(db_models.Group.id==i)]
    return todos


@RestRouter.post('/create_todo', response_model=pd_models.ToDo)
async def create_todo(todo: pd_models.ToDoBase,
                       user: JWTBearer = Depends(dep)):
    created = db_models.Todos.create(**todo.dict())
    return pd_models.ToDo(**model_to_dict(created, max_depth=0))


@RestRouter.post('/update_todo')
async def update_status(todo_new: pd_models.ToDo, user: JWTBearer = Depends(dep)):
    todo_check = db_models.Group.get(id=todo_new.group)
    todo = db_models.Todos(**todo_new.dict())
    if todo_check.user.username != user.username:
        return Response(status_code=403)
    todo.save()


@RestRouter.delete('/delete_todo/{todo_id}')
async def delete_todo(todo_id: int, user: pd_models.UserBase = Depends(dep)):
    todo = db_models.Todos.get(id=todo_id)
    if todo.group.user.username == user.username:
        todo.delete_instance()
