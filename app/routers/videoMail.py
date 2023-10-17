from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import FileResponse

from app.schema.schema import EmailSentSchema
from app.services.videoMail import VideoMailService
from app.utils.utils import BASE_URL

videoMailRouter = APIRouter()


@videoMailRouter.post("/")
def sendVideoMail(request: EmailSentSchema):
    return VideoMailService.sendMail(request)


@videoMailRouter.get("/user/{userId}")
def getVideoMails(userId: str):
    return {
        'sent': f'{BASE_URL}/videoMails/user/{userId}/sent',
        'received': f'{BASE_URL}/videoMails/user/{userId}/received'
    }


@videoMailRouter.get("/user/{userId}/sent")
def getSentVideoMails(userId: str):
    return VideoMailService.getSentVideoMails(userId)


@videoMailRouter.get("/user/{userId}/received")
def getReceivedVideoMails(userId: str):
    return VideoMailService.getReceivedVideoMails(userId)


@videoMailRouter.get("/{videoName}")
async def getVideoMail(videoName: str):
    return VideoMailService.getVideoFile(videoName)


@videoMailRouter.get("/covers/{videoName}")
async def getVideoMailCover(videoName: str):
    return VideoMailService.getCoverFile(videoName)