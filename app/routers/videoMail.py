from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import FileResponse

from app.schema.schema import EmailSentSchema
from app.services.videoMail import VideoMailService

videoMailRouter = APIRouter()


@videoMailRouter.post("/")
def sendVideoMail(request: EmailSentSchema):
    return VideoMailService.sendMail(request)


@videoMailRouter.get("/{videoName}")
async def getVideoMail(videoName: str):
    return VideoMailService.getVideoFile(videoName)


@videoMailRouter.get("/covers/{videoName}")
async def getVideoMailCover(videoName: str):
    return VideoMailService.getCoverFile(videoName)