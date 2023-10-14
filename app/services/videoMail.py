import requests
import base64

from app.model.repository.user import UserRepository
from app.schema.schema import EmailSentSchema
from app.services.user import UserService
from app.utils.errors.EmailNotSentException import EmailNotSentException
from app.utils.errors.GException import GException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.utils import createSuccessResponse, createErrorResponse


class VideoMailService:

    @classmethod
    def sendMail(cls, request: EmailSentSchema):

        try:
            user = UserRepository.getUserById(request.user_id)
            if user is None:
                raise UserNotFoundException()

            html_content = '''
                <html>
                    <body>
                        <h1>Your Video Email</h1>
                        <p>Video-email #334 by Alberto Di Maio</p>
                        <video width="320" height="240" controls>
                            <source src="'''+request.video_path+'''" type="video/mp4">
                            <div>
                                <p>Il tuo client non è supportato, perciò dovrai scaricare l'app per vedere il video-email</p>
                                <a href="'''+request.video_url+'''">
                                    <img src="'''+request.image_path+'''">
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
                    userReceiver = UserRepository.create(False, None, None, receiver, None, None)

                encoded_mail = base64.urlsafe_b64encode(
                    bytes(
                        f"Content-Type: text/html; charset=\"UTF-8\"\n" +
                        "MIME-Version: 1.0\n" +
                        "Content-Transfer-Encoding: base64\n" +
                        "to: "+receiver+"\n" +
                        "from: "+user.email+"\n" +
                        "subject: Subject Text\n\n" +
                        f"{base64.b64encode(html_content.encode()).decode('utf-8')}", 'utf-8'
                    )
                ).decode('utf-8')

                access_token = UserService.refreshToken(user, user.refresh_token)
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
            return createErrorResponse(GException)