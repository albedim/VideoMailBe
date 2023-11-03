from fastapi import APIRouter, Request
from starlette.responses import FileResponse

from app.configuration.config import authjwt
from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema, TokenData
from app.services.user import UserService

userRouter = APIRouter()


@userRouter.post("/complete")
async def complete(request: UserCompleteSchema):
    return UserService.completeUser(request)


@userRouter.post("/signin")
async def signin(request: UserSigninSchema):
    return UserService.signin(request)


@userRouter.post("/auth")
async def auth(request: UserAuthSchema):
    return UserService.auth(request)


@userRouter.get("/{userId}/stats")
async def getUserStats(userId: str):
    return UserService.getUserStats(userId)


@userRouter.get("/{userId}")
async def getUser(userId: str):
    return UserService.getUser(userId)


@userRouter.get("/{userId}/image")
async def getUserImage(userId: str):
    return UserService.getUserImage(userId)


@userRouter.post("/sync")
async def sync(request: Request):
    return UserService.sync(request.headers)