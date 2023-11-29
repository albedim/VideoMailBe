from sqlalchemy import text

from app.configuration.config import sql
from app.model.entity.user import User
from app.model.entity.videoMail import VideoMail
from app.model.repository.repo import Repository


class VideoMailRepository(Repository):

    @classmethod
    def create(cls, subject, path):
        videoMail: VideoMail = VideoMail(subject, path)
        sql.session.add(videoMail)
        cls.commit()
        return videoMail

    @classmethod
    def getSentVideoMails(cls, userId):
        videoMails = sql.session.query(VideoMail).from_statement(
            text("SELECT videoMails.* "
                 "FROM videoMails "
                 "JOIN sendings "
                 "ON videoMails.videoMail_id = sendings.videoMail_id "
                 "WHERE sendings.sender_id = :senderId "
                 "ORDER BY videoMails.sent_on DESC").params(senderId=userId)
        ).all()
        return videoMails

    @classmethod
    def getVideoMails(cls, userId):
        videoMails = sql.session.query(VideoMail).from_statement(
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
        videoMails = sql.session.query(VideoMail, User, text("favorite")).from_statement(
            text("SELECT videoMails.*, users.*, sendings.favorite "
                 "FROM videoMails "
                 "JOIN sendings "
                 "ON videoMails.videoMail_id = sendings.videoMail_id "
                 "JOIN users "
                 "ON sendings.sender_id = users.user_id "
                 "WHERE sendings.receiver_id = :senderId "
                 "ORDER BY videoMails.sent_on, sendings.favorite ASC").params(senderId=userId)
        ).all()
        return videoMails

    @classmethod
    def getFavoritedVideoMails(cls, userId):
        videoMails = sql.session.query(VideoMail, User).from_statement(
            text("SELECT videoMails.*, users.*"
                 "FROM videoMails "
                 "JOIN sendings "
                 "ON videoMails.videoMail_id = sendings.videoMail_id "
                 "JOIN users "
                 "ON sendings.sender_id = users.user_id "
                 "WHERE sendings.receiver_id = :senderId "
                 "AND sendings.favorite = true "
                 "ORDER BY videoMails.sent_on DESC").params(senderId=userId)
        ).all()
        return videoMails

    @classmethod
    def getVideoMail(cls, videoId):
        videoMail = sql.session.query(VideoMail).filter(VideoMail.videoMail_id == videoId).first()
        return videoMail
