from fastapi import APIRouter
from starlette.responses import FileResponse

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema
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