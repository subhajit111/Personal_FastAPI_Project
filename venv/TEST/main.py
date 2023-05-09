from TEST.database import engine, SessionLocal
from TEST import models
from distutils.core import setup
from xml.etree.ElementTree import fromstring
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test")
def test_func(db: Session = Depends(get_db)):
    return {"message":"success"}