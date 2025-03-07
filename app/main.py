from fastapi import FastAPI
import app.dependencies
from app.routers.v1 import users

app = FastAPI()

# รวม Routers
app.include_router(users.router)


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI with MongoDB!"}
