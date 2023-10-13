from http.client import HTTPException

import uvicorn

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.routers.videoMail import videoMailRouter
from app.utils.errors.MethodNotAllowedException import MethodNotAllowedException
from app.utils.errors.NotFoundException import NotFoundException
from app.utils.utils import createErrorResponse
from routers.user import userRouter
from app.configuration.config import Base, engine

app = FastAPI()
app.include_router(userRouter, prefix="/users")
app.include_router(videoMailRouter, prefix="/videoMails")


@app.get("/")
async def read_root():
    return {"Benvenuto": "VideoMail"}


@app.exception_handler(404)
async def custom_404_middleware(request, call_next):
    return createErrorResponse(NotFoundException)


@app.exception_handler(405)
async def custom_405_middleware(request, call_next):
    return createErrorResponse(MethodNotAllowedException)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
