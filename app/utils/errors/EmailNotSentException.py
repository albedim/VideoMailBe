from app.utils.errors.GException import GException


class EmailNotSentException(GException):
    message = "Email not sent exception"
    code = 400
