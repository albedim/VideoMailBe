from app.utils.errors.GException import GException


class FileNotFoundException(GException):
    message = "File not found exception"
    code = 404

