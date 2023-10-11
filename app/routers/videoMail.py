from fastapi import APIRouter

videoMailRouter = APIRouter()


@videoMailRouter.get("/")
def getAllVideoMails():
    return {
        "res": []
    }
