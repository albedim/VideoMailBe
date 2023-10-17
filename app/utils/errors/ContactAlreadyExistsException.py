from app.utils.errors.GException import GException


class ContactAlreadyExistsException(GException):
    message = "Contact already exists"
    code = 409