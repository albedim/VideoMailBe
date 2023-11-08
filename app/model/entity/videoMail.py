import datetime

from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class VideoMail(sql.Model):
    __tablename__ = 'videoMails'
    videoMail_id: int = sql.Column(sql.String(8), primary_key=True, autoincrement=False)
    subject: str = sql.Column(sql.String(34), nullable=False)
    code: str = sql.Column(sql.String(4), nullable=False)
    path: str = sql.Column(sql.String(54), nullable=False)
    sent_on: datetime.datetime = sql.Column(sql.DateTime, nullable=False)

    def __init__(self, subject, path):
        self.videoMail_id = generateUuid()
        self.subject = subject
        self.code = generateUuid(4)
        self.path = path
        self.sent_on = datetime.datetime.utcnow()

    def toJSON(self, **kvargs):
        obj = {
            'videoMail_id': self.videoMail_id,
            'subject': self.subject,
            'code': self.code,
            'path': f"{BASE_URL}/videoMails/videos/{self.videoMail_id}",
            'sent_on': str(self.sent_on),
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj