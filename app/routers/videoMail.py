from fastapi import APIRouter
from pydantic import BaseModel

from app.schema.schema import EmailSentSchema
from app.services.videoMail import VideoMailService

videoMailRouter = APIRouter()


@videoMailRouter.post("/")
def sendVideoMail(request: EmailSentSchema):
    return VideoMailService.sendMail(request)
