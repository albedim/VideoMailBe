from app.configuration.config import sql
from app.model.entity.contact import Contact
from app.model.repository.repo import Repository


class ContactRepository(Repository):

    @classmethod
    def create(cls, userId, contactId):
        contact: Contact = Contact(userId, contactId)
        sql.session.add(contact)
        cls.commit()
        return contact

    @classmethod
    def remove(cls, contact):
        sql.session.delete(contact)
        cls.commit()

    @classmethod
    def getContact(cls, user_id, contactId):
        contact = sql.session.query(Contact).filter(Contact.user_id == user_id).filter(Contact.contact_id == contactId).first()
        return contact