from flask import Flask, Blueprint, request

from app.schema.schema import UserCompleteSchema, ContactCreateSchema
from app.services.contact import ContactService

contactRouter: Blueprint = Blueprint('ContactController', __name__, url_prefix="/contacts")


@contactRouter.delete("/<userId>/<contactId>")
def remove(userId: str, contactId: str):
    return ContactService.remove(userId, contactId)


@contactRouter.post("/")
def create():
    return ContactService.create(request.json)


@contactRouter.get("/<userId>")
def getContacts(userId: str):
    return ContactService.getContacts(userId)