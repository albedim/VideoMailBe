from sqlalchemy import text

from app.configuration.config import Base, sql
from app.model.entity.sending import Sending
from app.model.entity.user import User
from app.utils.utils import generateUuid


class UserRepository:

    @classmethod
    def create(cls, registered, email, refreshToken):
        try:
            user: User = User(registered, email, refreshToken)
            sql.add(user)
            sql.commit()
            return user
        except Exception as exc:
            sql.rollback()

    @classmethod
    def getUserByEmail(cls, email):
        user = sql.query(User).filter(User.email == email).first()
        return user

    @classmethod
    def refreshToken(cls, user, token):
        try:
            user.access_token = token
            sql.commit()
            return user.access_token
        except Exception as exc:
            sql.rollback()

    @classmethod
    def getUserById(cls, user_id):
        user = sql.query(User).filter(User.user_id == user_id).first()
        return user

    @classmethod
    def completeUser(cls, profileImage, name, surname, password, user):
        try:
            user.name = name
            user.profile_image_path = profileImage
            user.surname = surname
            user.password = password
            user.completed = True
            user.registered = True
            user.completion_link = None
            sql.commit()
            return user
        except Exception as exc:
            sql.rollback()

    @classmethod
    def getUserByCompletionLink(cls, completion_link):
        user = sql.query(User).filter(User.completion_link == completion_link).first()
        return user

    @classmethod
    def signin(cls, email, password):
        user = sql.query(User).filter(User.email == email).filter(User.password == password).first()
        return user

    @classmethod
    def getContacts(cls, userId):
        contacts = sql.query(User).from_statement(
            text("SELECT users.* "
                 "FROM users "
                 "JOIN contacts "
                 "ON contacts.contact_id = users.user_id "
                 "WHERE contacts.user_id = :userId "
                 "ORDER BY users.email ASC").params(userId=userId)
        ).all()
        return contacts

    @classmethod
    def registerUser(cls, user, refreshToken):
        try:
            user.refresh_token = refreshToken
            user.registered = True
            sql.commit()
            return user
        except Exception as exc:
            sql.rollback()

    @classmethod
    def getReceivers(cls, videoMailId):
        users = sql.query(User, text("receiver_type")).from_statement(
            text("SELECT users.*, sendings.receiver_type "
                 "FROM users "
                 "JOIN sendings "
                 "ON sendings.receiver_id = users.user_id "
                 "WHERE sendings.videoMail_id = :videoMailId "
                 "ORDER BY sendings.receiver_type DESC").params(videoMailId=videoMailId)
        ).all()
        return users

    @classmethod
    def getSender(cls, videoMailId):
        user = sql.query(User).from_statement(
            text("SELECT users.* "
                 "FROM users "
                 "JOIN sendings "
                 "ON sendings.sender_id = users.user_id "
                 "WHERE sendings.videoMail_id = :videoMailId").params(videoMailId=videoMailId)
        ).first()
        return user