import uvicorn
from fastapi import FastAPI

from routers.hello import hello
from routers.test import test

app = FastAPI()
app.include_router(hello)
app.include_router(test)


@app.get("/")
async def read_root():
    return {"Benvenuto": "VideoMail"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
