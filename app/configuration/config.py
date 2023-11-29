from flask import Flask
from flask_jwt_extended import JWTManager
# from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from app.utils.errors.GException import GException
from app.utils.errors.MethodNotAllowedException import MethodNotAllowedException
from app.utils.errors.NotFoundException import NotFoundException

from app.utils.utils import getConnectionParameters
from app.utils.utils import createErrorResponse

params = getConnectionParameters("local")

# modules init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + params['user'] + ':' + params['password'] + '@' + params['host'] + '/' + params['db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['JWT_HEADER_NAME'] = 'Authorization'  # The name of the header that will carry the JWT token
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # The type of token in the header
app.config['JSON_SORT_KEYS'] = False
# scheduler = APScheduler()
sql = SQLAlchemy(app)
jwt = JWTManager(app)


@app.errorhandler(404)
def page_not_found(e):
    return createErrorResponse(NotFoundException)


@app.errorhandler(405)
def page_not_found(e):
    return createErrorResponse(MethodNotAllowedException)


@app.errorhandler(500)
def page_not_found(e):
    return createErrorResponse(GException)



