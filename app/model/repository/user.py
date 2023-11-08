from sqlalchemy import text

from app.configuration.config import sql
from app.model.entity.sending import Sending
from app.model.entity.user import User
from app.model.repository.repo import Repository
from app.utils.utils import generateUuid


class UserRepository(Repository):

    @classmethod
    def create(cls, registered, email, refreshToken):
        user: User = User(registered, email, refreshToken)
        sql.add(user)
        cls.commit()
        return user

    @classmethod
    def getUserByEmail(cls, email):
        user = sql.session.query(User).filter(User.email == email).first()
        return user

    @classmethod
    def refreshToken(cls, user, token):
        user.access_token = token
        cls.commit()
        return user.access_token

    @classmethod
    def getUserById(cls, user_id):
        user = sql.session.query(User).filter(User.user_id == user_id).first()
        return user

    @classmethod
    def completeUser(cls, profileImage, name, surname, password, user):
        user.name = name
        user.profile_image_path = profileImage
        user.surname = surname
        user.password = password
        user.completed = True
        user.completion_link = None
        cls.commit()
        return user

    @classmethod
    def getUserByCompletionLink(cls, completion_link):
        user = sql.session.query(User).filter(User.completion_link == completion_link).first()
        return user

    @classmethod
    def signin(cls, email, password):
        user = sql.session.query(User).filter(User.email == email).filter(User.password == password).first()
        return user

    @classmethod
    def getContacts(cls, userId):
        contacts = sql.session.query(User).from_statement(
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
        user.refresh_token = refreshToken
        user.registered = True
        user = cls.setCompletionLink(user)
        cls.commit()
        return user

    @classmethod
    def setCompletionLink(cls, user):
        user.completion_link = generateUuid(16)
        cls.commit()
        return user

    @classmethod
    def getReceivers(cls, videoMailId):
        users = sql.session.query(User, text("receiver_type")).from_statement(
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
        user = sql.session.query(User).from_statement(
            text("SELECT users.* "
                 "FROM users "
                 "JOIN sendings "
                 "ON sendings.sender_id = users.user_id "
                 "WHERE sendings.videoMail_id = :videoMailId").params(videoMailId=videoMailId)
        ).first()
        return user