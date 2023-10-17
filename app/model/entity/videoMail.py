import datetime

from sqlalchemy import String, Column, Date, Boolean
from app.configuration.config import Base
from app.utils.utils import generateUuid


class VideoMail(Base):
    __tablename__ = 'videoMails'
    videoMail_id: int = Column(String(8), primary_key=True, autoincrement=False)
    subject: str = Column(String(34), nullable=False)
    code: str = Column(String(4), nullable=False)
    path: str = Column(String(54), nullable=False)
    sent_on: datetime.date = Column(Date, nullable=False)

    def __init__(self, subject, path):
        self.videoMail_id = generateUuid()
        self.subject = subject
        self.code = generateUuid(4)
        self.path = path
        self.sent_on = datetime.date.today()

    def toJSON(self, **kvargs):
        obj = {
            'videoMail_id': self.videoMail_id,
            'subject': self.subject,
            'code': self.code,
            'path': self.path,
            'sent_on': str(self.sent_on),
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj