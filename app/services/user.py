import jwt
import requests
from google.oauth2 import id_token

from app.model.entity.user import User
from app.model.repository.user import UserRepository
from app.utils.errors.RefreshTokenNeededExceptiom import RefreshTokenNeededException
from app.utils.utils import createSuccessResponse, createErrorResponse, getClient


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
            res = cls.refreshToken(request.code, only_access_token=False)

            # in caso di errore vuol dire che l'utente continua a passare
            # un codice al posto di un refresh_token

            if 'error' in res and res['error'] == 'invalid_grant':
                return createErrorResponse(RefreshTokenNeededException), RefreshTokenNeededException.code

            userInformation = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+res['id_token']).json()
            user = UserRepository.getUserByEmail(userInformation['email'])
            return createSuccessResponse({
                'user': user.toJSON(),
                'new': False
            })
        else:
            userInformation = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+res['id_token']).json()
            createdUser = UserRepository.create(
                True,
                request.name,
                request.surname,
                userInformation['email'],
                res['refresh_token']
            )
            return createSuccessResponse({
                'user': createdUser.toJSON(),
                'new': True
            })

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