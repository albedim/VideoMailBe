from sqlalchemy import text

from app.configuration.config import Base, sql
from app.model.entity.contact import Contact


class ContactRepository:

    @classmethod
    def create(cls, userId, contactId):
        contact: Contact = Contact(userId, contactId)
        sql.add(contact)
        sql.commit()
        return contact

    @classmethod
    def remove(cls, contact):
        sql.delete(contact)
        sql.commit()

    @classmethod
    def getContact(cls, user_id, contactId):
        contact = sql.query(Contact).filter(Contact.user_id == user_id).filter(Contact.contact_id == contactId).first()
        return contact