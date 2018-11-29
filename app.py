import os
from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import config
from api import api_blueprint

api = Api(api_blueprint)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv('SECRET_KEY')
    JWTManager(app)

    # register blueprint
    app.register_blueprint(api_blueprint)

    # import views
    import api.views

    return app
