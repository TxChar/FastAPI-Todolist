from fastapi import FastAPI
import app.dependencies

from app.routers.v1 import tasks, sub_tasks

app = FastAPI()

app.include_router(tasks.router)
app.include_router(sub_tasks.router)


# @app.get("/")
# def home():
#     return {"message": "Welcome to FastAPI with MongoDB!"}
