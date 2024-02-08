from fastapi import FastAPI

from .routers import post, user, auth
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine) #creates all tables, if it doesnt already exists

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}



