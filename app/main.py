from fastapi import FastAPI
import app.dependencies

from app.routers.v1 import subtask, tasks

app = FastAPI()

app.include_router(tasks.router)
app.include_router(subtask.router)


# @app.get("/")
# def home():
#     return {"message": "Welcome to FastAPI with MongoDB!"}
