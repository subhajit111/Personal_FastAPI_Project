# this file is used for creating JWT tokens
from jose import JWTError, jwt
from datetime import datetime, timedelta
from TEST import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= '/login')

# secret_key can be anything but the more complex it is the better and it is unique to your api only
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# in this func we are passing a dict of values 
# later on we are adding exire which hold the current time + the amount of time after which the token will be expired
def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # this is a function in jwt which takes 3 values and creates a token and returns it.
    # you can check this token's content in jwt website
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# this function is used to decode and varify the data the user have sent
def varify_access_token(token: str, credentials_exceptions):

    # try and except is alz good for the code that could error out
    # here we are using jwt.decode() method to decode the token that has been cteated by the create_access_token
    # once we decode the token we are retriving the data that we have passed in auth.py fie which is userid
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id : str = payload.get("userid")

        # here we are chcecking we are getting the data
        # once we have the id we are checking if the id value is correct as per our schemas file
        if id is None:
            raise credentials_exceptions
        
        token_data = schemas.Token_data(id= id)
    
    # uf we have any error while decoding the token we can we JWTError to raise and error warning
    except JWTError:
        raise credentials_exceptions

    return token_data


# this function actually calls the varify_access_token funtion where all our logic is written to decode the incoming token and varify the data
def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"could not validate the credentials", 
    headers= {"WWW-Authenticate": "Bearer"})

    return varify_access_token(token, credentials_exceptions)