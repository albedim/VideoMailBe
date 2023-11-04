from http.client import HTTPException

import uvicorn

from fastapi import Request, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.middleware.cors import CORSMiddleware

from app.routers.sending import sendingRouter
from app.routers.test import test
from app.routers.videoMail import videoMailRouter
from app.utils.errors.MethodNotAllowedException import MethodNotAllowedException
from app.utils.errors.NotFoundException import NotFoundException
from app.utils.utils import createErrorResponse, BASE_URL
from routers.user import userRouter
from routers.contact import contactRouter
from app.configuration.config import Base, engine, sql

app = FastAPI()

app.include_router(userRouter, prefix="/users")
app.include_router(test, prefix="/test")
app.include_router(contactRouter, prefix="/contacts")
app.include_router(sendingRouter, prefix="/sendings")
app.include_router(videoMailRouter, prefix="/videoMails")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://videomail.pages.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root(request: Request):
    return {'documentation': f"{BASE_URL}/docs"}


@app.exception_handler(404)
async def custom_404_middleware(request, call_next):
    return createErrorResponse(NotFoundException)


@app.exception_handler(405)
async def custom_405_middleware(request, call_next):
    return createErrorResponse(MethodNotAllowedException)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, port=8000)
