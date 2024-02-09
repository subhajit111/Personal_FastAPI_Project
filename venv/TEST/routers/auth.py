from codecs import utf_16_le_decode
from dataclasses import dataclass
import email
from statistics import mode
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from TEST.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # this helps to get data in a certain format {"username": "", "password": ""}
from TEST import schemas, util, models, Oauth2

router = APIRouter(
    tags=['Authentication']
)

# create a new function login of user
# user_credentials : schemas.Login -- gets the user input like email and passowrd as per the schema format
# instead of useing schemas for input format we are using OAuth2PasswordRequestForm which has a dict with values username and password
# no matter what the user send in the data field it will be stored as username and password
# if the username and password is correct then only we are passing the id(from the database) as a value which is user.id stored in new_accesstoken
# this new_accesstoken then passed as a input while creating the token encryption 

@router.get("/login", response_model= schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    
    # this user is a dict which retrives the user credentials stored in the database only if username and password matches
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    # this if statement takes the usergiven-password and the database stored password and checks them if they are similar
    # vairity_pass() func takes the user-given password and converts into hash and then checks the stored hash in the database for similarity
    if not util.varify_pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")
    

    # this create_access_token got imported from Oauth2.py file where this function takes the data and if it matches then retuens a new token
    new_accesstoken = Oauth2.create_access_token(data= {"userid": user.id})

    return {"token": new_accesstoken, "tokentype": "bearer"}
