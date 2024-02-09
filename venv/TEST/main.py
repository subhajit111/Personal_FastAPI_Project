from TEST.database import engine, SessionLocal, get_db
from TEST import models, database
from fastapi import FastAPI,Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from TEST.routers import post, users, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# this object is used to connect to the specific routers of other files like post.router, users.router
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
