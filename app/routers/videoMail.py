from fastapi import Request, APIRouter
from pydantic import BaseModel
from starlette.responses import FileResponse

from app.schema.schema import EmailSentSchema, FavoriteVideoMailSchema
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


@videoMailRouter.post("/favorite")
def favoriteVideoMail(request: FavoriteVideoMailSchema):
    return VideoMailService.favourite(request)


@videoMailRouter.get("/user/{userId}/favorited")
def getReceivedVideoMails(userId: str):
    return VideoMailService.getFavoritedVideoMails(userId)


@videoMailRouter.get("/user/{userId}/received")
def getReceivedVideoMails(userId: str):
    return VideoMailService.getReceivedVideoMails(userId)


@videoMailRouter.get("/{videoId}")
async def getVideoMail(request: Request, videoId: str):
    return VideoMailService.getVideo(request.headers, videoId)


@videoMailRouter.get("/videos/{videoId}")
async def getVideoMailFile(videoId: str):
    return VideoMailService.getVideoFile(videoId)


@videoMailRouter.get("/covers/{videoId}")
async def getVideoMailCoverFile(videoId: str):
    return VideoMailService.getCoverFile(videoId)