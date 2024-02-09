---
id: 734xk167u34z9u6tdo90hf0
title: main.py
desc: ''
updated: 1707424784533
created: 1707250228471
---

## To run the app use "uviron main:app --reload"
- --reload makes the code uptodata so we dont have to run the query multipletimes

#--reload is for dev only. Dont use in prod environments. 

### Here we are creating a instance of fastapi
app = FastAPI()

- The function name can be anything

- In the return statement whateve you write fastapi automatically converts it json coz that is the universal language for APIs.

- @app.get("/") - this is a path operation which acts as a decorator. A decorator is something that takes a function and perfome some operation on top of it.

- .get is a http method we are using for this path operation which is ("/") or ("/<anything>")

- This /anything inside the () means user have to go to this path for the operation

- ### Always remember for a specific https method fastapi will always look for the first path operation.
- What it means if i have 2 get with ("/") - same path operation then only the first one will showup. 

- ### Fastapi looks for the method like "get" then looks for the path like ("/") then it return the result 

- Post method is used to create new datas. 
- when we use post method with a bunch of info our api will read the data and create a new field in database.

## Post method
- _**def create_posts(message: dict = Body)**_ : Here  we are retriving the Body [where the user pass the value]
- **We are importing the body from fastAPI.**
- We are storing the value as a dict in message and then printing it.

