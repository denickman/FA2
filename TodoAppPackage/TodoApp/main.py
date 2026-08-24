import models
from database import engine
from fastapi import FastAPI
from routers import auth, todos

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)



# check JWT tokens
# https://jwt.io