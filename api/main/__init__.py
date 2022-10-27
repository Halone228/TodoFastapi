from fastapi import APIRouter
RestRouter = APIRouter(prefix='/api')

from . import todos, groups

RestRouter.include_router(todos.RestRouter)
RestRouter.include_router(groups.RestRouter)



