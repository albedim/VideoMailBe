import jwt
import requests
from google.oauth2 import id_token

from app.model.entity.user import User
from app.model.repository.user import UserRepository
from app.utils.errors.GException import GException
from app.utils.errors.RefreshTokenNeededExceptiom import RefreshTokenNeededException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException
from app.utils.errors.UserNotCompletedException import UserNotCompletedException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse, getClient, hashString


class UserService:

    @classmethod
    def auth(cls, request):

        # chiamati api (oauth2) per ricevere un access_token e un refresh_token
        # dal codice ricevuto dal frontend

        res = requests.post("https://oauth2.googleapis.com/token", json={
            "client_id": getClient()['client_id'],
            "client_secret": getClient()['client_secret'],
            "code": request.code.replace("%", "/"),
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000"
        }).json()

        # in caso di errore vuol dire che l'utente ha già usato un codice
        # e se vuole riloggare deve usare un refresh_token

        if 'error' in res and res['error'] == 'invalid_grant':
            return createErrorResponse(UnAuthorizedException)

        userInformation = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+res['id_token']).json()
        createdUser = UserRepository.create(True, userInformation['email'], res['refresh_token'])
        return createSuccessResponse({
            'complete_account_code': createdUser.completion_link
        })

    @classmethod
    def signin(cls, request):
        try:
            user = UserRepository.getUserByEmail(request.email)

            if user is None:
                raise UserNotFoundException()
            if not user.completed:
                raise UserNotCompletedException()
            if user.password == hashString(request.password):
                return createSuccessResponse(user.toJSON())
            else:
                raise UserNotFoundException()

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except UserNotCompletedException as exc:
            return createErrorResponse(UserNotCompletedException)
        except Exception as exc:
            return createErrorResponse(GException)

    @classmethod
    def completeUser(cls, request):
        try:
            user = UserRepository.getUserByCompletionLink(request.completion_link)

            if user is None:
                raise UserNotFoundException()
            user = UserRepository.completeUser(request.name, request.surname, hashString(request.password), user)
            return createSuccessResponse(user.toJSON())

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except UnAuthorizedException as exc:
            return createErrorResponse(UnAuthorizedException)
        except Exception as exc:
            return createErrorResponse(GException)

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

        if only_access_token:
            return res['access_token']
        return res