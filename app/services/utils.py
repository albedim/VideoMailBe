import yaml
import string
import random
import uuid


def getConnectionParameters(datasource):
        with open('../config/config.yaml', 'r') as f:
            data = yaml.load(f,  Loader=yaml.FullLoader)
            for ds in data['datasources']:
                if ds["name"] == datasource:
                    return {"user": ds["user"],
                            "password": ds["password"],
                            "host": ds["host"],
                            "port": ds["port"],
                            "db": ds["db"]}
            raise Exception("Connection not found")


def generatePinCode(size=6, chars=string.digits) :
        return ''.join(random.choice(chars) for x in range(size))


def generateUuid(size=8) :
    return str(uuid.uuid4())[:size]