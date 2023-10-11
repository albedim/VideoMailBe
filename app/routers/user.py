from fastapi import APIRouter

userRouter = APIRouter()


@userRouter.get("/")
def getAllUsers():
    return {
        "res": []
    }
