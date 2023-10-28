from app.utils.errors.GException import GException


class VideoMailNotFoundException(GException):
    message = "This videoMail doesn't exist"
    code = 404