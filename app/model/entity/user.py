import datetime

from sqlalchemy import String, Column, Date
from app.configuration.config import Base
from app.utils.utils import generateUuid


class User(Base):
    __tablename__ = 'users'
    user_id: int = Column(String(14), primary_key=True, autoincrement=False)
    name: str = Column(String(34), nullable=True)
    surname: str = Column(String(34), nullable=True)
    email: str = Column(String(43), nullable=False)
    access_token: str = Column(String(140), nullable=True)
    refresh_token: str = Column(String(140), nullable=True)
    created_on: datetime.date = Column(Date, nullable=False)

    def __init__(self, name, surname, email, refreshToken, accessToken):
        self.user_id = generateUuid()
        self.email = email
        self.surname = surname
        self.name = name
        self.access_token = accessToken
        self.refresh_token = refreshToken
        self.created_on = datetime.date.today()

    def toJSON(self, **kvargs):
        obj = {
            'user_id': self.user_id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'created_on': str(self.created_on),
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj