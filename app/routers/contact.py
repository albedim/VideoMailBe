from fastapi import APIRouter

from app.schema.schema import UserCompleteSchema, ContactCreateSchema
from app.services.contact import ContactService

contactRouter = APIRouter()


@contactRouter.delete("/{userId}/{contactId}")
async def create(userId: str, contactId: str):
    return ContactService.remove(userId, contactId)


@contactRouter.post("/")
async def create(request: ContactCreateSchema):
    return ContactService.create(request)


@contactRouter.get("/{userId}")
async def getContacts(userId: str):
    return ContactService.getContacts(userId)