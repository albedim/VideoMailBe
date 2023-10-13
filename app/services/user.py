import requests

from app.utils.utils import createSuccessResponse


class UserService:

    @classmethod
    def auth(cls, request):
        # ... salvare utente nel database con access_token
        res = requests.post("https://oauth2.googleapis.com/token", json={
            "client_id": "651229141185-egfqcebnr2a5bdll5r04lfrg1t03fms1.apps.googleusercontent.com",
            "client_secret": "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",
            "code": request.code.replace("%", "/"),
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000"
        }).json()
        return createSuccessResponse(res)

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