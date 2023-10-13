import requests
import base64

from app.utils.errors.EmailNotSentException import EmailNotSentException
from app.utils.utils import createSuccessResponse, createErrorResponse


class VideoMailService:

    @classmethod
    def sendMail(cls, request):
        # l'utente dovrebbe essere gettato tramite l'user_id
        user = {
            "email": "dimaio.albe@gmail.com",
            "access_token": 'ya29.a0AfB_byBCBMXkaXQ9629g3nqfn4iut7YFwPJE1f0HBGmLJ1Wl1DZK_hXXqTW7HsXOH-K57za_GIdy5tunp0T0kgOaUF8mC8c02wjGHpNahTWFzCC8NZ1SsMJI9bhntY41aupHtlK203g31Jl432VMS8yMYjHquKA6rDIUaCgYKAaESARMSFQGOcNnCOaOiwgtRfNAYlVsMNcdj5g0171'
        }

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

        encoded_mail = base64.urlsafe_b64encode(
            bytes(
                f"Content-Type: text/html; charset=\"UTF-8\"\n" +  # Specify HTML content type
                "MIME-Version: 1.0\n" +
                "Content-Transfer-Encoding: base64\n" +  # Use base64 encoding
                "to: "+request.receiver_email+"\n" +
                "from: "+user['email']+"\n" +
                "subject: Subject Text\n\n" +
                f"{base64.b64encode(html_content.encode()).decode('utf-8')}", 'utf-8'  # Encode HTML content
            )
        ).decode('utf-8')

        access_token = user['access_token']

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'raw': encoded_mail
        }
        response = requests.post('https://www.googleapis.com/gmail/v1/users/me/messages/send', headers=headers, json=data)

        if response.status_code == 200:
            return createSuccessResponse('Email successfully sent')
        else:
            return createErrorResponse(EmailNotSentException), EmailNotSentException.code

