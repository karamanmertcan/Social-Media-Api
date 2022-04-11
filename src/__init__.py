import mongoengine
from flask import Flask, jsonify
from flask_restful import Api
import os
from src.auth import Me, Register, Login
import certifi

from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask_jwt_extended import JWTManager

from src.post import UserPosts


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("dev"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )

    else:
        app.config.from_mapping(test_config)

    JWTManager(app)

    mongoengine.connect(
        host='mongodb+srv://mertcankaraman:mertcan123@cluster0.zujdj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true', tlsCAFile=certifi.where())

    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Me, '/api/auth/me')
    api.add_resource(UserPosts, '/api/user/post')

    @app.route("/")
    def hello_api():
        return jsonify({"message": "Welcome to the API"})

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong"}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
