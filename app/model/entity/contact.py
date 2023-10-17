import datetime

from sqlalchemy import String, Column, Date, Boolean, ForeignKey
from app.configuration.config import Base
from app.utils.utils import generateUuid


class Contact(Base):
    __tablename__ = 'contacts'
    user_id: str = Column(String(8), ForeignKey("users.user_id"), primary_key=True, autoincrement=False)
    contact_id: str = Column(String(8), ForeignKey("users.user_id"), primary_key=True, nullable=True)

    def __init__(self, user_id, contact_id):
        self.user_id = user_id
        self.contact_id = contact_id

    def toJSON(self, **kvargs):
        obj = {
            'user_id': self.user_id,
            'name': self.name,
            'registered': self.registered,
            'completion_link': self.completion_link,
            'completed': self.completed,
            'surname': self.surname,
            'email': self.email,
            'refresh_token': self.refresh_token,
            'created_on': str(self.created_on),
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj