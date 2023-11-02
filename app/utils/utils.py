import base64
import hashlib
import os
from datetime import datetime
from http.client import HTTPException

import cv2
import jwt
import yaml
import string
import random
import uuid

from fastapi.security import OAuth2PasswordBearer
from moviepy.video.io.VideoFileClip import VideoFileClip
from starlette.responses import JSONResponse
from app.utils.errors.GException import GException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException


def getConnectionParameters(datasource):
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for ds in data['datasources']:
            if ds["name"] == datasource:
                return {"user": ds["user"],
                        "password": ds["password"],
                        "host": ds["host"],
                        "port": ds["port"],
                        "db": ds["db"]}
        raise Exception("Connection not found")


def getVariables(datasource):
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for ds in data['variables']:
            if ds['name'] == datasource:
                return ds


def generatePinCode(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generateUuid(size=8):
    return str(uuid.uuid4())[:size]


def hashString(password: str):
    return hashlib.md5(password.encode('UTF-8')).hexdigest()


def createSuccessResponse(param):
    return {
        "date": str(datetime.now()),
        "success": True,
        "param": param,
        "code": 200,
    }


def getClient():
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return {
            'client_id': data['client']['client_id'],
            'client_secret': data['client']['client_secret']
        }


def getFormattedDateTime():
    return datetime.now().__str__() \
        .replace("-", "") \
        .replace(" ", "") \
        .replace(":", "") \
        .replace(".", "")


def createErrorResponse(error):
    return JSONResponse({
        "date": str(datetime.now()),
        "success": False,
        "error": {
            "message": error.message,
            "path": error.__module__
        },
        "code": error.code,
    }, error.code)


def createJWTToken(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "super-secret", algorithm="HS256")
    return encoded_jwt


def isTokenValid(headers):
    try:
        if headers.get("Authorization") is None:
            return False
        if 'Bearer' not in headers.get("Authorization"):
            return False
        tokenPayload = jwt.decode(headers.get("Authorization").split(" ")[1], key="super-secret")
        return True
    except Exception:
        return False


"""
:description: Decodifica un video in base64 e lo salva
:param videoPath: str
:return: None
"""


def saveFile(base64Data, filePath):
    try:
        decoded_data = base64.b64decode(base64Data)
        with open(filePath, 'wb') as file:
            file.write(decoded_data)
    except Exception as exc:
        ...


BASE_URL = getVariables('local')['BASE_URL']
