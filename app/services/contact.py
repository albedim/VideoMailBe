import jwt
import requests
from google.oauth2 import id_token

from app.model.entity.user import User
from app.model.repository.contact import ContactRepository
from app.model.repository.user import UserRepository
from app.utils.errors.ContactAlreadyExistsException import ContactAlreadyExistsException
from app.utils.errors.ContactNotFoundException import ContactNotFoundException
from app.utils.errors.GException import GException
from app.utils.errors.RefreshTokenNeededExceptiom import RefreshTokenNeededException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException
from app.utils.errors.UserNotCompletedException import UserNotCompletedException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse, getClient, hashString, BASE_URL


class ContactService:

    @classmethod
    def getContacts(cls, userId):
        try:
            user = UserRepository.getUserById(userId)

            if user is None:
                raise UserNotFoundException()

            contacts = UserRepository.getContacts(userId)
            print(contacts)
            res = []
            for contact in contacts:
                res.append(contact.toJSON())
            return createSuccessResponse(res)

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def create(cls, request):
        try:
            user = UserRepository.getUserById(request.user_id)
            contactUser = UserRepository.getUserByEmail(request.contact_email)

            if user is None:
                raise UserNotFoundException()
            if not user.registered or not user.completed:
                raise UnAuthorizedException()
            if contactUser is None:
                contactUser = UserRepository.create(False, request.contact_email, None)
            else:
                if contactUser.user_id == user.user_id:
                    raise UnAuthorizedException()

            contact = ContactRepository.getContact(user.user_id, contactUser.user_id)
            if contact is not None:
                raise ContactAlreadyExistsException()

            ContactRepository.create(request.user_id, contactUser.user_id)
            return createSuccessResponse("Contact successfully created")
        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except UnAuthorizedException as exc:
            return createErrorResponse(UnAuthorizedException)
        except ContactAlreadyExistsException as exc:
            return createErrorResponse(ContactAlreadyExistsException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def remove(cls, user_id, contact_id):
        try:
            contact = ContactRepository.getContact(user_id, contact_id)

            if contact is None:
                raise ContactNotFoundException()

            ContactRepository.remove(contact)
            return createSuccessResponse("Contact successfully removed")
        except ContactNotFoundException as exc:
            return createErrorResponse(ContactNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))