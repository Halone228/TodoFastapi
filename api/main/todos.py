from fastapi import Depends, Request, Response
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


@RestRouter.post('/update_status/{todo_id}')
async def update_status(todo_id: int, req: Request, user: JWTBearer = Depends(dep)):
    status = (await req.json()).get('status')
    if status is None:
        return Response(status_code=500,content={
            'error': 'Dont set status'
        })
    todo = db_models.Todos.get(id=todo_id)
    todo.status = status
    todo.save()


@RestRouter.delete('/delete_todo/{todo_id}')
async def delete_todo(todo_id: int, user: pd_models.UserBase = Depends(dep)):
    todo = db_models.Todos.get(id=todo_id)
    if todo.group.user.username == user.username:
        todo.delete_instance()