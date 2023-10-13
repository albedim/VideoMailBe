import jwt
import requests
from google.oauth2 import id_token

from app.model.repository.user import UserRepository
from app.utils.errors.RefreshTokenNeededExceptiom import RefreshTokenNeededException
from app.utils.utils import createSuccessResponse, createErrorResponse


class UserService:

    @classmethod
    def create(cls, request):
        UserRepository.create("aa", "asfsa", "sgas", "sgas", "sgsa")
        return createSuccessResponse("aa")

    @classmethod
    def auth(cls, request):

        res = requests.post("https://oauth2.googleapis.com/token", json={
            "client_id": "651229141185-egfqcebnr2a5bdll5r04lfrg1t03fms1.apps.googleusercontent.com",
            "client_secret": "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",
            "code": request.code.replace("%", "/"),
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000"
        }).json()
        print(res)
        if 'error' in res and res['error'] == 'invalid_grant':
            res = requests.post("https://oauth2.googleapis.com/token", json={
                "client_id": "651229141185-egfqcebnr2a5bdll5r04lfrg1t03fms1.apps.googleusercontent.com",
                "client_secret": "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",
                "refresh_token": request.code,
                "grant_type": "refresh_token",
                "redirect_uri": "http://localhost:3000"
            }).json()

            if 'error' in res and res['error'] == 'invalid_grant':
                return createErrorResponse(RefreshTokenNeededException), RefreshTokenNeededException.code

            userInformation = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+res['id_token']).json()
            print(userInformation)
            user = UserRepository.getUserByEmail(userInformation['email'])
            updatedUser = UserRepository.refreshToken(user, res['access_token'])
            return createSuccessResponse({
                'user': updatedUser.toJSON(),
                'new': False
            })
        else:
            userInformation = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+res['id_token']).json()
            print(userInformation)
            createdUser = UserRepository.create(request.name, request.surname, userInformation['email'], request.code, res['access_token'])
            return createSuccessResponse({
                'user': createdUser.toJSON(),
                'new': True
            })

    @classmethod
    def refresh(cls, request):
        # ... salvare utente nel database
        res = requests.post("https://oauth2.googleapis.com/token", json={
            "client_id": "651229141185-egfqcebnr2a5bdll5r04lfrg1t03fms1.apps.googleusercontent.com",
            "client_secret": "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",
            "refresh_token": request.refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": "http://localhost:3000"
        }).json()
        return createSuccessResponse(res)