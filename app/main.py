from fastapi import FastAPI
from app.routers import post,users, auth, vote
from . import models     
from .database import engine
from .config import setting
from fastapi.middleware.cors import CORSMiddleware 
#use it to manually create table amd db updates replaced by alembic (data migration tool)
# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = [
          # "https://www.google.com"
          ]
##### Middleware #####
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


##### Routers #####

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/get")
def hello_Message():
     return {"message": "Welcome to my api  "}





