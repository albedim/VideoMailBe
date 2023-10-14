from app.configuration.config import Base, sql
from app.model.entity.user import User


class UserRepository:

    @classmethod
    def create(cls, registered, name, surname, email, refreshToken, accessToken):
        user: User = User(registered, name, surname, email, refreshToken, accessToken)
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