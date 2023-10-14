from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    code: str
    name: str
    surname: str


class UserRefreshSchema(BaseModel):
    refresh_token: str


class EmailSentSchema(BaseModel):
    video: str
    receiver_emails: list[str]
    user_id: str
    subject: str