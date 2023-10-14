from app.configuration.config import Base, sql
from app.model.entity.user import User


class UserRepository:

    @classmethod
    def create(cls, registered, email, refreshToken):
        user: User = User(registered, email, refreshToken)
        sql.add(user)
        sql.commit()
        return user

    @classmethod
    def getUserByEmail(cls, email):
        user = sql.query(User).filter(User.email == email).first()
        return user

    @classmethod
    def refreshToken(cls, user, token):
        user.access_token = token
        sql.commit()
        return user.access_token

    @classmethod
    def getUserById(cls, user_id):
        user = sql.query(User).filter(User.user_id == user_id).first()
        return user

    @classmethod
    def completeUser(cls, name, surname, password, user):
        user.name = name
        user.surname = surname
        user.password = password
        user.completed = True
        user.completion_link = None
        sql.commit()
        return user

    @classmethod
    def getUserByCompletionLink(cls, completion_link):
        user = sql.query(User).filter(User.completion_link == completion_link).first()
        return user

    @classmethod
    def signin(cls, email, password):
        user = sql.query(User).filter(User.email == email).filter(User.password == password).first()
        return user