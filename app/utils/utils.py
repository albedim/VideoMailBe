import base64
import hashlib
import os
from datetime import datetime

import cv2
import yaml
import string
import random
import uuid

from moviepy.video.io.VideoFileClip import VideoFileClip
from starlette.responses import JSONResponse

from app.utils.errors.GException import GException


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


BASE_URL = getVariables('local')['BASE_URL']
