from TEST import models, schemas, util, Oauth2
from TEST.database import engine, get_db
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter()

@router.get("/allusers", response_model= List[schemas.Response_User])
def test_func(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model= schemas.Response_User)
def create_user(users : schemas.Create_user ,db : Session = Depends(get_db)):
    
    #hash the password
    hashed_password = util.hash(users.password)
    users.password = hashed_password
    
    new_user = models.Users(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/singleuser/{id}", response_model= schemas.Response_User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} not found")
    else:
        return user


@router.delete("/deleteuser/{id}")
def delete_user(id: int, db : Session = Depends(get_db), userid: int = Depends(Oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/updateuser/{id}", status_code= status.HTTP_200_OK)
def update_user(users: schemas.Create_user ,id: int, db : Session = Depends(get_db), userid : int = Depends(Oauth2.get_current_user)):
    hashed_password = util.hash(users.password)
    users.password = hashed_password
    
    user_query = db.query(models.Users).filter(models.Users.id == id)

    user = user_query.first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    user_query.update(users.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()