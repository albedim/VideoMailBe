from sqlalchemy import text

from app.configuration.config import Base, sql
from app.model.entity.user import User
from app.model.entity.videoMail import VideoMail


class VideoMailRepository:

    @classmethod
    def create(cls, subject, path):
        videoMail: VideoMail = VideoMail(subject, path)
        sql.add(videoMail)
        sql.commit()
        return videoMail

    @classmethod
    def getSentVideoMails(cls, userId):
        videoMails = sql.query(VideoMail, User).from_statement(
            text("SELECT videoMails.*, users.* "
                 "FROM videoMails "
                 "JOIN sendings "
                 "ON videoMails.videoMail_id = sendings.videoMail_id "
                 "JOIN users "
                 "ON sendings.receiver_id = users.user_id "
                 "WHERE sendings.sender_id = :senderId").params(senderId=userId)
        ).all()
        return videoMails

    @classmethod
    def getVideoMails(cls, userId):
        videoMails = sql.query(VideoMail).from_statement(
            text("SELECT videoMails.* "
                 "FROM videoMails "
                 "JOIN sendings "
                 "ON videoMails.videoMail_id = sendings.videoMail_id "
                 "WHERE sendings.sender_id = :senderId "
                 "OR sendings.receiver_id = :senderId").params(senderId=userId)
        ).all()
        return videoMails

    @classmethod
    def getReceivedVideoMails(cls, userId):
        videoMails = sql.query(VideoMail, User).from_statement(
            text("SELECT videoMails.*, users.* "
                 "FROM videoMails "
                 "JOIN sendings "
                 "ON videoMails.videoMail_id = sendings.videoMail_id "
                 "JOIN users "
                 "ON sendings.sender_id = users.user_id "
                 "WHERE sendings.receiver_id = :senderId ").params(senderId=userId)
        ).all()
        return videoMails