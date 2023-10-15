from app.utils.errors.GException import GException


class ContactNotFoundException(GException):
    message = "Contact not found"
    code = 404