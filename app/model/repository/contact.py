from sqlalchemy import text

from app.configuration.config import Base, sql
from app.model.entity.contact import Contact
from app.model.repository.repo import Repository


class ContactRepository(Repository):

    @classmethod
    def create(cls, userId, contactId):
        contact: Contact = Contact(userId, contactId)
        sql.add(contact)
        cls.commit()
        return contact

    @classmethod
    def remove(cls, contact):
        sql.delete(contact)
        cls.commit()

    @classmethod
    def getContact(cls, user_id, contactId):
        contact = sql.query(Contact).filter(Contact.user_id == user_id).filter(Contact.contact_id == contactId).first()
        return contact