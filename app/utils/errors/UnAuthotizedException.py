from app.utils.errors.GException import GException


class UnAuthorizedException(GException):
    message = "You are not authorized to perform this action"
    code = 403
