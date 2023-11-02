from app.utils.errors.GException import GException


class TokenExpiredException(GException):
    message = "The token you provided is expired"
    code = 422
