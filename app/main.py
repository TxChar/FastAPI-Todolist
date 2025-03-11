from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.config.database
from app.routers.v1 import subtask, tasks, auth


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(subtask.router)


# @app.get("/")
# def home():
#     return {"message": "Welcome to FastAPI with MongoDB!"}
