import datetime
import os.path

import cv2
import requests
import base64

from starlette.responses import FileResponse

from app.model.repository.sending import SendingRepository
from app.model.repository.videoMail import VideoMailRepository
from app.model.repository.user import UserRepository
from app.schema.schema import EmailSentSchema
from app.services.user import UserService
from app.utils.errors.EmailNotSentException import EmailNotSentException
from app.utils.errors.FileNotFoundEcxeption import FileNotFoundException
from app.utils.errors.GException import GException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse, generateUuid, getFormattedDateTime


class VideoMailService:

    @classmethod
    def sendMail(cls, request: EmailSentSchema):

        try:
            user = UserRepository.getUserById(request.user_id)

            if user is None:
                raise UserNotFoundException()
            if not user.completed:
                raise UnAuthorizedException()

            videoName = getFormattedDateTime()
            videoPath = "files/videomails/"+videoName+".mp4"
            cls.saveFile(request.video, videoPath)
            cls.extractVideoCover(videoPath)
            videoMail = VideoMailRepository.create(request.subject, videoPath)
            print(videoMail.toJSON())
            html_content = '''
                <html>
                    <body>
                        <h1>Your Video Email</h1>
                        <p>Video-email #334 by Alberto Di Maio</p>
                        <video width="320" height="240" controls>
                            <source src="http://localhost:8000/videoMails/''' + videoName + '''.mp4" type="video/mp4">
                            <div>
                                <p>Il tuo client non è supportato, perciò dovrai scaricare l'app per vedere il video-email</p>
                                <a href="http://localhost:3000/videoMails/#343535">
                                    <img src="http://localhost:8000/videoMails/covers''' + videoName + '''.jpeg">
                                </a>
                            </div>
                        </video>
                    </body>
                </html>
            '''

            receivers = []
            for receiver in request.receiver_emails:

                userReceiver = UserRepository.getUserByEmail(receiver)
                if userReceiver is None:
                    userReceiver = UserRepository.create(False, receiver, None)

                sending = SendingRepository.create("a", videoMail.videoMail_id, userReceiver.user_id, user.user_id)
                encoded_mail = base64.urlsafe_b64encode(
                    bytes(
                        f"Content-Type: text/html; charset=\"UTF-8\"\n" +
                        "MIME-Version: 1.0\n" +
                        "Content-Transfer-Encoding: base64\n" +
                        "to: " + receiver + "\n" +
                        "from: " + user.email + "\n" +
                        "subject: " + request.subject + "\n\n" +
                        f"{base64.b64encode(html_content.encode()).decode('utf-8')}", 'utf-8'
                    )
                ).decode('utf-8')

                access_token = UserService.refreshToken(user.refresh_token)
                response = requests.post(
                    'https://www.googleapis.com/gmail/v1/users/me/messages/send',
                    headers={
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'raw': encoded_mail
                    }
                )

                if response.status_code == 200:
                    receivers.append(receiver)

            if len(receivers) != len(request.receiver_emails):
                if len(receivers) > 0:
                    return createSuccessResponse({
                        'message': 'Email only sent to some of the receivers',
                        'receivers': receivers,
                        'errors': True
                    })
                else:
                    raise EmailNotSentException()

            return createSuccessResponse({
                'message': 'Email successfully sent',
                'receivers': receivers,
                'errors': False
            })

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except EmailNotSentException as exc:
            return createErrorResponse(EmailNotSentException)
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException)

    @classmethod
    def getSentVideoMails(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()

            videoMails = VideoMailRepository.getSentVideoMails(userId)
            res = []
            for videoMail in videoMails:
                path = videoMail[0].path.split("/")[-1]
                res.append(videoMail[0].toJSON(receiver=videoMail[1], path="http://localhost:8000/videoMails/"+path))

            return createSuccessResponse({
                'sender': user.toJSON(),
                'videoMails': res
            })
        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException)

    @classmethod
    def getReceivedVideoMails(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()

            videoMails = VideoMailRepository.getReceivedVideoMails(userId)
            res = []
            for videoMail in videoMails:
                path = videoMail[0].path.split("/")[-1]
                res.append(videoMail[0].toJSON(sender=videoMail[1], path="http://localhost:8000/videoMails/"+path))

            return createSuccessResponse({
                'receiver': user.toJSON(),
                'videoMails': res
            })
        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException)

    @classmethod
    def getVideoFile(cls, videoName):
        if os.path.exists(os.path.join(os.getcwd(), "files/videomails/" + videoName)):
            return FileResponse(os.path.join(os.getcwd(), "files/videomails/" + videoName),
                                media_type='video/mp4')
        else:
            return createErrorResponse(FileNotFoundException)

    @classmethod
    def getCoverFile(cls, videoName):
        if os.path.exists("files/covers/" + videoName):
            return FileResponse("files/covers/" + videoName,
                                media_type='image/png')
        else:
            return createErrorResponse(FileNotFoundException)

    @classmethod
    def saveFile(cls, base64Data, filePath):
        try:
            decoded_data = base64.b64decode(base64Data)
            with open(filePath, 'wb') as file:
                file.write(decoded_data)
            return True
        except Exception as exc:
            print(exc)
            return False

    @classmethod
    def extractVideoCover(cls, videoPath):
        try:
            count = 0
            vidcap = cv2.VideoCapture(videoPath)
            success, image = vidcap.read()
            success = True
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
            success, image = vidcap.read()
            cv2.imwrite(videoPath.replace("videomails", "covers").replace("mp4", "jpeg"),
                        image)  # save frame as JPEG file
        except Exception as e:
            print(e)
            return False
