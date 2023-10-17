from app.utils.errors.GException import GException


class MethodNotAllowedException(GException):
    message = "This method is not allowed"
    code = 405
