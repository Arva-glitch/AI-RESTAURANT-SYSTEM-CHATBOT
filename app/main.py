from app.models import *
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from app.database import SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.database import Base


# -------------------------------Import all models-----------------------------------------------------

from app.models import *


# ------------------------------------------------------------------------------------------------------
# creating an attribute of fastapi
app = FastAPI(title="Restaurant Chatbot API")  # , version="1.0.0"

# ----------used this to tell mysql to uk create database and load all the table-------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(Base.metadata.tables.keys())
    # Base.metadata.create_all(bind=engine)
    print("Database Created Successfully")

    yield

    print("Application Shutdown")


app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
def home():
    return {"message": "Restaurant Chatbot API"}

# ------------------------------------------------------------------------------------------------------
