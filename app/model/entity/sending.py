import datetime
import enum

from sqlalchemy import String, Column, Date, Boolean, Enum, ForeignKey
from app.configuration.config import Base
from app.utils.utils import generateUuid


class Sending(Base):
    __tablename__ = 'sendings'
    sender_id: int = Column(String(8), ForeignKey('users.user_id'), primary_key=True, autoincrement=False)
    receiver_id: str = Column(String(8), ForeignKey('users.user_id'), primary_key=True, autoincrement=False)
    favorite: bool = Column(Boolean, nullable=False)
    videoMail_id: str = Column(String(8), ForeignKey('videoMails.videoMail_id'), primary_key=True, autoincrement=False)
    receiver_type: enum = Column(Enum("a", "cc"), nullable=False)

    def __init__(self, receiver_type, sender_id, receiver_id, videoMail_id):
        self.receiver_type = receiver_type
        self.sender_id = sender_id
        self.favorite = False
        self.receiver_id = receiver_id
        self.videoMail_id = videoMail_id

    def toJSON(self, **kvargs):
        obj = {
            'videoMail_id': self.videoMail_id,
            'subject': self.subject,
            'code': self.code,
            'path': self.path,
            'created_on': str(self.created_on),
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj