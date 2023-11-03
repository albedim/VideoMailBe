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

    @classmethod
    def get(cls, user_id, videoMail_id):
        sending = sql.query(Sending).filter(Sending.receiver_id == user_id).filter(Sending.videoMail_id == videoMail_id).first()
        return sending

    @classmethod
    def favorite(cls, sending):
        sending.favorite = not sending.favorite
        sql.commit()
        return sending