from flask import Blueprint, request

from app.schema.schema import EmailSentSchema, FavoriteVideoMailSchema
from app.services.videoMail import VideoMailService
from app.utils.utils import BASE_URL

videoMailRouter: Blueprint = Blueprint('VideoMailController', __name__, url_prefix="/videoMails")


@videoMailRouter.post("/")
def sendVideoMail():
    return VideoMailService.sendMail(request.json)


@videoMailRouter.get("/user/<userId>")
def getVideoMails(userId: str):
    return {
        'sent': f'{BASE_URL}/videoMails/user/{userId}/sent',
        'received': f'{BASE_URL}/videoMails/user/{userId}/received'
    }


@videoMailRouter.get("/user/<userId>/sent")
def getSentVideoMails(userId: str):
    return VideoMailService.getSentVideoMails(userId)


@videoMailRouter.post("/favorite")
def favoriteVideoMail():
    return VideoMailService.favourite(request.json)


@videoMailRouter.get("/user/<userId>/favorited")
def getFavoriteVideoMails(userId: str):
    return VideoMailService.getFavoritedVideoMails(userId)


@videoMailRouter.get("/user/<userId>/received")
def getReceivedVideoMails(userId: str):
    return VideoMailService.getReceivedVideoMails(userId)


@videoMailRouter.get("/<videoId>")
def getVideoMail(videoId: str):
    return VideoMailService.getVideo(request.headers, videoId)


@videoMailRouter.get("/videos/<videoId>")
def getVideoMailFile(videoId: str):
    return VideoMailService.getVideoFile(videoId)


@videoMailRouter.get("/covers/<videoId>")
def getVideoMailCoverFile(videoId: str):
    return VideoMailService.getCoverFile(videoId)