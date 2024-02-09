from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/get_posts")
def get_posts():
    return {"Posts": "Here are your posts"}

@app.post("/create_posts")
def create_posts(message: dict = Body):
    print(message['Title'], message['Name'])
    return {"New post": f"Titel = {message['Title']}, Name = {message['Name']}"}