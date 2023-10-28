from fastapi import FastAPI
from app.services.utils import getConnectionParameters, generatePinCode,generateUuid
from fastapi import APIRouter
from app.services.qrCodeGenerator import QRCodeGenerator

test = APIRouter()


@test.get("/sendMail")
async def sendMail():
    param = getConnectionParameters("local")
    return {"sendMail": param["user"]}


@test.get("/getPinCode")
async def getPinCode():
    pin = generatePinCode()
    return {"Pin": pin}


@test.get("/getUuid")
async def getUuid():
    uuid = generateUuid()
    return {"Uuid": uuid}


@test.get("/getQrCode")
async def getQrCode():
    qr = QRCodeGenerator()
    a = qr.create(generateUuid(), generatePinCode())
    print(a)
    return {"Creazione": a}



