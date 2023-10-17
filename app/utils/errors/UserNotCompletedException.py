from app.utils.errors.GException import GException


class UserNotCompletedException(GException):
    message = "User not completed"
    code = 422