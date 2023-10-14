from fastapi import APIRouter
from starlette.responses import FileResponse

from app.schema.schema import UserAuthSchema, UserRefreshSchema
from app.services.user import UserService

userRouter = APIRouter()


@userRouter.post("/auth")
async def auth(request: UserAuthSchema):
    return UserService.auth(request)