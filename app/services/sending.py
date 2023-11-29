import datetime
import os.path
import requests
import base64

from app.model.repository.sending import SendingRepository
from app.model.repository.user import UserRepository
from app.schema.schema import EmailSentSchema
from app.services.user import UserService
from app.utils.errors.EmailNotSentException import EmailNotSentException
from app.utils.errors.FileNotFoundEcxeption import FileNotFoundException
from app.utils.errors.GException import GException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse, generateUuid, getFormattedDateTime


class SendingService:

    ...
