from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    code: str


class UserRefreshSchema(BaseModel):
    refresh_token: str


class EmailSentSchema(BaseModel):
    video: str
    receiver_emails: list[str]
    user_id: str
    subject: str


class UserCompleteSchema(BaseModel):
    name: str
    surname: str
    password: str
    completion_link: str


class UserSigninSchema(BaseModel):
    email: str
    password: str


class ContactCreateSchema(BaseModel):
    user_id: str
    contact_email: str