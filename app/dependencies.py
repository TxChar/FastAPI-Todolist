import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "")

connect(db=DB_NAME, host=MONGO_URI, alias="default")
