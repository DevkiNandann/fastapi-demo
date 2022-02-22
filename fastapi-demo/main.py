from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, auth


app = FastAPI()

# creates the table in db
models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
