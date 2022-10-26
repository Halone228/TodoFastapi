import uvicorn
import database
from fastapi import FastAPI
from api import RestRouter,AuthRouter


database.init()


app = FastAPI()


app.include_router(AuthRouter)
app.include_router(RestRouter)








