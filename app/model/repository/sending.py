from app.configuration.config import Base, sql
from app.model.entity.user import User
from app.model.entity.sending import Sending
from app.model.repository.repo import Repository


class SendingRepository(Repository):

    @classmethod
    def create(cls, receiverType, videoMailId, receiverId, senderId):
        sending: Sending = Sending(receiverType, senderId, receiverId, videoMailId)
        sql.add(sending)
        cls.commit()
        return sending

    @classmethod
    def remove(cls, sending):
        sql.delete(sending)
        cls.commit()

    @classmethod
    def get(cls, user_id, videoMail_id):
        sending = sql.query(Sending).filter(Sending.receiver_id == user_id).filter(Sending.videoMail_id == videoMail_id).first()
        return sending

    @classmethod
    def favorite(cls, sending):
        sending.favorite = not sending.favorite
        cls.commit()
        return sending