from fastapi import APIRouter

hello = APIRouter()

class Hello(str):
    @hello.get("/hello")
    def hello(self):
        return {"Hello": self}