from app.utils.errors.GException import GException


class InvalidSchemaException(GException):
    message = "Invalid schema exception"
    code = 400
