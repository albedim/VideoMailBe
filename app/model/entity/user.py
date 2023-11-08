import datetime

from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class User(sql.Model):
    __tablename__ = 'users'
    user_id: int = sql.Column(sql.String(8), primary_key=True, autoincrement=False)
    name: str = sql.Column(sql.String(46), nullable=True)
    profile_image_path: str = sql.Column(sql.String(54), nullable=True)
    registered: bool = sql.Column(sql.Boolean, nullable=False)
    completion_link: str = sql.Column(sql.String(16), nullable=True)
    password: str = sql.Column(sql.String(140), nullable=True)
    completed: bool = sql.Column(sql.Boolean, nullable=False)
    surname: str = sql.Column(sql.String(46), nullable=True)
    email: str = sql.Column(sql.String(62), nullable=False)
    refresh_token: str = sql.Column(sql.String(140), nullable=True)
    created_on: datetime.datetime = sql.Column(sql.DateTime, nullable=False)

    def __init__(self, registered, email, refreshToken):
        self.user_id = generateUuid()
        self.email = email
        self.profile_image_path = "files/profileimages/default.png"
        self.registered = registered
        self.completed = False
        self.refresh_token = refreshToken
        self.created_on = datetime.datetime.utcnow()

    def toJSON(self, **kvargs):
        obj = {
            'user_id': self.user_id,
            'name': self.name,
            'registered': self.registered,
            'completion_link': self.completion_link,
            'profile_image_path': f"{BASE_URL}/users/{self.user_id}/image",
            'completed': self.completed,
            'surname': self.surname,
            'email': self.email,
            'refresh_token': self.refresh_token,
            'created_on': str(self.created_on),
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj