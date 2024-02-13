from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import post, user, auth, vote
from . import models
from .database import engine

# Not really needed again, because 'alembic' does this for us now
models.Base.metadata.create_all(bind=engine) #creates all tables, if it doesnt already exists

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}



