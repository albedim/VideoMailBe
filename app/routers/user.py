from fastapi import APIRouter
from app.schema.schema import UserAuthSchema, UserRefreshSchema
from app.services.user import UserService

userRouter = APIRouter()


@userRouter.post("/auth")
async def auth(request: UserAuthSchema):
    return UserService.auth(request)


@userRouter.post("/refresh")
async def refresh(request: UserRefreshSchema):
    return UserService.refresh(request)