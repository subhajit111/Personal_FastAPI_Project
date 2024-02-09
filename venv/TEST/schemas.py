import email
from time import time
from unicodedata import name
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# EmailStr -- automatically detects the porper formatting of the user input for the email format
# the first class make sure the user provides the right values in correct format
# second class is used for defining the data send back to the user

class Create_user(BaseModel):
    email : EmailStr
    password : str
class Response_User(BaseModel):
    id : int
    email : EmailStr
    password : str
    create_at : datetime
    
    class Config:
        orm_mode = True




class Posts(BaseModel):
    name : str
    content : str
class Postresponse(BaseModel):
    id : int
    name : str
    content: str
    create_at : datetime

    class Config:
        orm_mode = True


class Login(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    token : str
    tokentype : str

class Token_data(BaseModel):
    id : Optional[str] = None