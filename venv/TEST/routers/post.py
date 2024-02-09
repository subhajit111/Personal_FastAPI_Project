from TEST import models, schemas, util, Oauth2
from TEST.routers import auth
from TEST.Oauth2 import get_current_user
from TEST.database import engine, get_db
from click import get_current_context
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional


#router creates the api just like api = FastAPI()
#we have to call this router in the main file and all the https methods will be called by this
router = APIRouter()



# this gets all the posts in the database
# response_model= List[schemas.Postresponse] -- returns all the data in a list format and follows the schemas.Postresponse format
# db: Session = Depends(get_db) -- used to create the database instance

@router.get("/posts", response_model= List[schemas.Postresponse])
def all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


# add a single post into the database
# models.Posts(**post.dict()) -- this automatically gets all the user data and assign them to newpost as a dictonary
# db.add(new_post) -- this add the new_post which is a dict into the database
# db.commit() -- commits the data into database
# userid use a Dependency from Oauth2 file called get_current_user for validating the user credentials(this will be retrived from 
#  the token and after the decoding the token)


@router.post("/addpost",status_code=status.HTTP_201_CREATED)
def add_post(post : schemas.Posts, db: Session = Depends(get_db),userid : int = Depends(Oauth2.get_current_user)):
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# .first() -- gets the first response that matches without going through all
# raise HTTPException -- helps to send response back to the user in postman

@router.get("/singlepost/{id}", response_model= schemas.Postresponse)
def get_single_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    return post


# in delete methods we should not send back any data so we only returning the response to user

@router.delete("/deletepost/{id}")
def delete_posts(id: int, db : Session = Depends(get_db), userid: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# posts: schemas.Posts -- get the data from user in proper format mentioned in schemas
# save the user input into a dict 
# post_query.update(posts.dict(), synchronize_session=False) -- automatically matches and changes the required field

@router.put("/updatepost/{id}",response_model= schemas.Postresponse)
def update_posts(posts: schemas.Posts ,id: int, db : Session = Depends(get_db), userid : int = Depends(Oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    post_query.update(posts.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
