from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.configuration.config import sql, app
from app.routers import contact, user, sending, videoMail
from app.utils.utils import BASE_URL


app.register_blueprint(contact.contactRouter)
app.register_blueprint(user.userRouter)
app.register_blueprint(sending.sendingRouter)
app.register_blueprint(videoMail.videoMailRouter)

CORS(app, resources={r"*": {"origins": ["http://localhost", "http://localhost:3000", "https://videomailfe.pages.dev"]}})


@app.route("/")
def read_root():
    return jsonify({'documentation': f"{BASE_URL}/docs"})


def create_app():
    with app.app_context():
        sql.create_all()
    return app


if __name__ == "__main__":
    create_app().run(port=8000)
