import datetime
import os
from datetime import timedelta

import jwt
import requests
from flask import send_file
from flask_jwt_extended import create_access_token

from app.configuration.config import sql
from app.model.entity.user import User
from app.model.repository.repo import Repository
from app.model.repository.sending import SendingRepository
from app.model.repository.user import UserRepository
from app.model.repository.videoMail import VideoMailRepository
from app.utils.errors.FileNotFoundEcxeption import FileNotFoundException
from app.utils.errors.GException import GException
from app.utils.errors.RefreshTokenNeededExceptiom import RefreshTokenNeededException
from app.utils.errors.TokenExpiredException import TokenExpiredException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException
from app.utils.errors.UserNotCompletedException import UserNotCompletedException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse, getClient, hashString, createJWTToken, BASE_URL, \
    isTokenValid, saveFile, getFormattedDateTime


class UserService:

    @classmethod
    def auth(cls, request):

        # chiamati api (oauth2) per ricevere un access_token e un refresh_token
        # dal codice ricevuto dal frontend

        res = requests.post("https://oauth2.googleapis.com/token", json={
            "client_id": getClient()['client_id'],
            "client_secret": getClient()['client_secret'],
            "code": request['code'].replace("%", "/"),
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000"
        }).json()

        # in caso di errore vuol dire che l'utente ha già usato un codice
        # e se vuole riloggare deve usare un refresh_token

        if 'error' in res and res['error'] == 'invalid_grant':
            return createErrorResponse(UnAuthorizedException)

        userInformation = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token=" + res['id_token']).json()

        user = UserRepository.getUserByEmail(userInformation['email'])
        if user is None:
            createdUser = UserRepository.create(True, userInformation['email'], res['refresh_token'])
            createdUser = UserRepository.setCompletionLink(createdUser)
        else:
            createdUser = UserRepository.registerUser(user, res['refresh_token'])
            createdUser = UserRepository.setCompletionLink(createdUser)

        return createSuccessResponse({
            'complete_account_code': createdUser.completion_link
        })

    @classmethod
    def getUserStats(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()
            videoMails = len(VideoMailRepository.getSentVideoMails(userId))
            return createSuccessResponse({
                'sent_videoMails': videoMails,
                'from': str(user.created_on),
                'to': str(datetime.datetime.now()).split(".")[0]
            })
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def getUser(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()
            return createSuccessResponse(user.toJSON())
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def signin(cls, request):
        try:
            user = UserRepository.getUserByEmail(request['email'])

            if user is None:
                raise UserNotFoundException()
            if not user.completed:
                raise UserNotCompletedException()
            if user.password == hashString(request['password']):
                return createSuccessResponse({
                    'token': create_access_token(identity={'user_id': user.user_id, 'expires_in': 14}, expires_delta=timedelta(days=14))
                })
            else:
                raise UserNotFoundException()

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except UserNotCompletedException as exc:
            return createErrorResponse(UserNotCompletedException)
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException(exc))

    @classmethod
    def completeUser(cls, request):
        try:
            user = UserRepository.getUserByCompletionLink(request['completion_link'])

            if user is None:
                raise UserNotFoundException()
            if not user.registered:
                raise UnAuthorizedException()
            if user.completed:
                raise UserNotFoundException()
            profileImage = "files/profileimages/default.png"
            if request['profile_image'] != "":
                imageName = getFormattedDateTime() + ".png"
                profileImage = f"files/profileimages/{imageName}"
                saveFile(request['profile_image'], profileImage)

            user = UserRepository.completeUser(profileImage, request['name'], request['surname'],
                                               hashString(request['password']), user)
            return createSuccessResponse({
                'token': create_access_token(identity={'user_id': user.user_id, 'expires_in': 14}, expires_delta=timedelta(days=14))
            })

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except UnAuthorizedException as exc:
            return createErrorResponse(UnAuthorizedException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def refreshToken(
            cls,
            refreshToken: str,
            only_access_token=True
    ):
        res = requests.post("https://oauth2.googleapis.com/token", json={
            "client_id": getClient()['client_id'],
            "client_secret": getClient()['client_secret'],
            "refresh_token": refreshToken,
            "grant_type": "refresh_token",
            "redirect_uri": "http://localhost:3000"
        }).json()
        print(res)
        if only_access_token:
            return res['access_token']
        return res

    @classmethod
    def getUserImage(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()
            if os.path.exists(os.path.abspath(user.profile_image_path)):
                return send_file(os.path.abspath(user.profile_image_path))
            else:
                return createErrorResponse(FileNotFoundException)
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)

    @classmethod
    def sync(cls, tokenSub):
        try:
            user = UserRepository.getUserById(tokenSub['user_id'])
            if user is None:
                raise UserNotFoundException()
            return createSuccessResponse(True)
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except jwt.exceptions.ExpiredSignatureError:
            return createErrorResponse(TokenExpiredException())
        except jwt.exceptions.DecodeError:
            return createErrorResponse(UnAuthorizedException())
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException(exc))

    @classmethod
    def isReceiverOrSender(cls, userId, videoMailId):
        receivers = UserRepository.getReceivers(videoMailId)
        sender = UserRepository.getSender(videoMailId)
        user = UserRepository.getUserById(userId)
        isReceiver = False
        for e in receivers:
            if e[0].email == user.email:
                isReceiver = True
        if isReceiver:
            return True
        return user == sender
