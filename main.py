import uvicorn
import database
from fastapi import FastAPI
from api import RestRouter, AuthRouter
from fastapi.middleware.cors import CORSMiddleware

database.init()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter)
app.include_router(RestRouter)

def start_dev():
    uvicorn.run(app, reload=True)

#uvicorn.run(app)
