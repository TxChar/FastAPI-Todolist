from fastapi import FastAPI
import app.dependencies
from app.routers.v1 import users, tasks

app = FastAPI()

# รวม Routers
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI with MongoDB!"}
