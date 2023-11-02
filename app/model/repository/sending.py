from app.configuration.config import Base, sql
from app.model.entity.user import User
from app.model.entity.sending import Sending


class SendingRepository:

    @classmethod
    def create(cls, receiverType, videoMailId, receiverId, senderId):
        try:
            sending: Sending = Sending(receiverType, senderId, receiverId, videoMailId)
            sql.add(sending)
            sql.commit()
            return sending
        except Exception as exc:
            sql.rollback()

    @classmethod
    def remove(cls, sending):
        try:
            sql.delete(sending)
            sql.commit()
        except Exception as exc:
            sql.rollback()