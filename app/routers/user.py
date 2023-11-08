from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema, TokenData
from app.services.user import UserService

userRouter: Blueprint = Blueprint('UserController', __name__, url_prefix="/users")


@userRouter.post("/complete")
def complete():
    return UserService.completeUser(request.json)


@userRouter.post("/signin")
def signin():
    return UserService.signin(request.json)


@userRouter.post("/auth")
def auth():
    return UserService.auth(request.json)


@userRouter.get("/<userId>/stats")
def getUserStats(userId: str):
    return UserService.getUserStats(userId)


@userRouter.get("/<userId>")
def getUser(userId: str):
    return UserService.getUser(userId)


@userRouter.get("/<userId>/image")
def getUserImage(userId: str):
    return UserService.getUserImage(userId)


@userRouter.post("/sync")
@jwt_required()
def sync():
    return UserService.sync(get_jwt_identity())