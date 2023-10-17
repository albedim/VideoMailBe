from app.utils.errors.GException import GException


class NotFoundException(GException):
    message = "This page was not found"
    code = 404
