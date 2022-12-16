from fastapi import APIRouter
RestRouter = APIRouter(prefix='/api')

from . import todos, groups, user

RestRouter.include_router(todos.RestRouter)
RestRouter.include_router(groups.RestRouter)
RestRouter.include_router(user.RestRouter)



