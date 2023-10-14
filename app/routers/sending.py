from fastapi import APIRouter
from starlette.responses import FileResponse

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema
from app.services.sending import SendingService

sendingRouter = APIRouter()