from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    code: str
    name: str
    surname: str


class UserRefreshSchema(BaseModel):
    refresh_token: str


class EmailSentSchema(BaseModel):
    video_path: str
    video_url: str
    image_path: str
    receiver_email: str

