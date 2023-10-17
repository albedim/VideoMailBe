from app.utils.errors.GException import GException


class UserNotFoundException(GException):
    message = "This user was not found"
    code = 404
