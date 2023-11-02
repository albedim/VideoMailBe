from app.configuration.config import Base, sql
from app.model.entity.user import User
from app.model.entity.sending import Sending


class SendingRepository:

    @classmethod
    def create(cls, receiverType, videoMailId, receiverId, senderId):
        sending: Sending = Sending(receiverType, senderId, receiverId, videoMailId)
        sql.add(sending)
        sql.commit()
        return sending

    @classmethod
    def remove(cls, sending):
        sql.delete(sending)
        sql.commit()