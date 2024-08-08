from fastapi import FastAPI
from app.routers import task, user
from app.db import engine
from app.models import Base, Task, User


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
print(CreateTable(User.__table__))