class UserAuthSchema():
    code: str


class UserRefreshSchema():
    refresh_token: str


class ReceiverSchema():
    email: str
    type: str


class EmailSentSchema():
    video: str
    receiver_emails: list[ReceiverSchema]
    user_id: str
    subject: str


class UserCompleteSchema():
    name: str
    surname: str
    profile_image: str
    password: str
    completion_link: str


class UserSigninSchema():
    email: str
    password: str


class ContactCreateSchema():
    user_id: str
    contact_email: str


class TokenData():
    user_id: str


class FavoriteVideoMailSchema():
    user_id: str
    videoMail_id: str
