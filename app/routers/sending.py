from flask import Blueprint

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema
from app.services.sending import SendingService

sendingRouter: Blueprint = Blueprint('SendingController', __name__, url_prefix="/sendings")