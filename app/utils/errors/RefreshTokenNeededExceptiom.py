from app.utils.errors.GException import GException


class RefreshTokenNeededException(GException):
    message = "This user already tried to log in. If you want to log in you need to use your refresh token"
    code = 403