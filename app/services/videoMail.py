import datetime
import os.path

import cv2
import jwt
import requests
import base64

from flask import send_file

from app.configuration.config import sql
from app.model.repository.repo import Repository
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
from app.utils.errors.VideoMailNotFoundException import VideoMailNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse, generateUuid, getFormattedDateTime, BASE_URL, \
    isTokenValid, saveFile


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
            videoPath = "files/videomails/" + videoName + ".webm"
            saveFile(request.video, videoPath)
            # cls.extractVideoCover(videoPath, "")
            videoMail = VideoMailRepository.create(request.subject, videoPath)

            html_content = '''
                <html>
                    <body>
                        <h1>VideoMail #'''+videoMail.videoMail_id+'''</h1>
                        <p>Ti è stato mandato un nuovo VideoMail da '''+ user.name + ' ' + user.surname+'''</p>
                        <video width="320" height="240" controls>
                            <source src="http://localhost:8000/videoMails/videos/''' + videoMail.videoMail_id + '''" type="video/webm">
                            <div>
                                <p>Il tuo client non è supportato, perciò dovrai scaricare l'app per vedere il VideoMail <br> 
                                Ecco il pin di accesso nel caso ti dovesse essere richiesto</p>
                                <h2>'''+videoMail.code+'''</h2>
                                <a href="http://localhost:3000/videoMails/'''+videoMail.videoMail_id+'''">
                                    <img src="http://localhost:8000/videoMails/covers/''' + videoMail.videoMail_id + '''">
                                </a>
                            </div>
                        </video>
                    </body>
                </html>
            '''

            receivers = []
            for receiver in request.receiver_emails:

                userReceiver = UserRepository.getUserByEmail(receiver.email)
                if userReceiver is None:
                    userReceiver = UserRepository.create(False, receiver.email, None)

                sending = SendingRepository.create(receiver.type, videoMail.videoMail_id, userReceiver.user_id, user.user_id)
                encoded_mail = base64.urlsafe_b64encode(
                    bytes(
                        f"Content-Type: text/html; charset=\"UTF-8\"\n" +
                        "MIME-Version: 1.0\n" +
                        "Content-Transfer-Encoding: base64\n" +
                        "to: " + userReceiver.email + "\n" +
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
                else:
                    SendingRepository.remove(sending)

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
            return createErrorResponse(GException(exc))


    @classmethod
    def getSentVideoMails(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()

            videoMails = VideoMailRepository.getSentVideoMails(userId)
            res = []
            for videoMail in videoMails:
                receivers = UserRepository.getReceivers(videoMail.videoMail_id)
                for i in range(len(receivers)):
                    receivers[i] = receivers[i][0].toJSON(receiver_type=receivers[i][1])
                res.append(
                    videoMail.toJSON(receivers=receivers)
                )

            return createSuccessResponse({
                'sender': user.toJSON(),
                'videoMails': res
            })
        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))


    @classmethod
    def getReceivedVideoMails(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()

            videoMails = VideoMailRepository.getReceivedVideoMails(userId)
            res = []
            for videoMail in videoMails:
                res.append(
                    videoMail[0].toJSON(favorite=bool(videoMail[2]), sender=videoMail[1].toJSON())
                )

            return createSuccessResponse({
                'receiver': user.toJSON(),
                'videoMails': res
            })
        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    """
    :description: Crea una file response di un video
    :param videoName: str
    :return: dict | FileResponse
    """

    @classmethod
    def getVideoFile(cls, videoId):
        try:
            videoMail = VideoMailRepository.getVideoMail(videoId)

            if videoMail is not None and os.path.exists(videoMail.path):
                return send_file("../" + videoMail.path)
            else:
                return createErrorResponse(FileNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    """
    :description: Crea una file response della copertina di un video
    :param videoName: str
    :return: dict | FileResponse
    """

    @classmethod
    def getCoverFile(cls, videoId):
        videoMail = VideoMailRepository.getVideoMail(videoId)

        if videoMail is not None and os.path.exists(videoMail.path.replace("videomails", "covers")):
            return send_file("../" + videoMail.path.replace("videomails", "covers"))
        else:
            return createErrorResponse(FileNotFoundException)

    """
    :description: Estrae un frame da un video e lo salva come file jpeg
    :param videoPath: str
    :return: None
    """

    @classmethod
    def extractVideoCover(cls, videoPath, frame_number):
        try:
            vidcap = cv2.VideoCapture(videoPath)

            # Check if the video file was successfully opened
            if not vidcap.isOpened():
                print("a")
                raise Exception("Failed to open video file")

            # Get the total number of frames in the video
            total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

            if frame_number >= total_frames:
                print("aaa")
                raise Exception("Invalid frame number. Frame number exceeds the total number of frames.")
            # Set the frame to extract
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, image = vidcap.read()

            if success:
                # Customize the output file name and path
                output_path = videoPath.replace("videomails", "covers").replace("webm", "jpeg")
                cv2.imwrite(output_path, image)
            else:
                print("aaa")
                raise Exception("Failed to extract the cover image.")

            # Release the video capture object when done
            vidcap.release()
        except Exception as e:
            print(f"Error: {str(e)}")

    @classmethod
    def getVideo(cls, headers, videoId):
        videoMail = VideoMailRepository.getVideoMail(videoId)

        if videoMail is None:
            raise VideoMailNotFoundException()

        if not isTokenValid(headers):
            return createSuccessResponse({
                'authorized': True,
                'pin_required': True,
                'videoMail': videoMail.toJSON(
                    path=f"{BASE_URL}/videoMails/videos/{videoMail.videoMail_id}")
            })

        tokenPayload = jwt.decode(headers.get("Authorization").split(" ")[1], key="super-secret")
        authorized = UserService.isReceiverOrSender(tokenPayload['user_id'], videoId)
        return createSuccessResponse({
            'authorized': authorized,
            'pin_required': False,
            'videoMail': videoMail.toJSON(
            path=f"{BASE_URL}/videoMails/videos/{videoMail.videoMail_id}")
        })

    @classmethod
    def favourite(cls, request):
        try:
            videoMail = VideoMailRepository.getVideoMail(request.videoMail_id)

            if videoMail is None:
                raise VideoMailNotFoundException()

            sending = SendingRepository.get(request.user_id, request.videoMail_id)
            SendingRepository.favorite(sending)

            return createSuccessResponse("Favorite")
        except VideoMailNotFoundException:
            return createErrorResponse(VideoMailNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def getFavoritedVideoMails(cls, userId):
        try:
            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()

            videoMails = VideoMailRepository.getFavoritedVideoMails(userId)
            res = []
            for videoMail in videoMails:
                res.append(
                    videoMail[0].toJSON(sender=videoMail[1].toJSON())
                )

            return createSuccessResponse({
                'receiver': user.toJSON(),
                'videoMails': res
            })
        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException(exc))