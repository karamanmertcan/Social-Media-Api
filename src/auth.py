from flask_restful import Resource, reqparse
from flask import jsonify, request
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


class Login(Resource):

    def post(self):
        email = request.json['email']
        password = request.json['password']

        user = User.objects(email=email).first()

        if user:
            user_password = user['password']
            is_password_correct = check_password_hash(
                user_password, password)

            if is_password_correct:
                return user.to_json()

        return {
            "message": "User not found"
        }


class Register(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('firstName', type=str, required=True)
        parser.add_argument('lastName', type=str, required=True)
        args = parser.parse_args()

        username = args['username']
        email = args['email']
        password = args['password']
        firstName = args['firstName']
        lastName = args['lastName']

        user = User.objects(username=username).first()

        if user:
            return {
                "message": "User already exists"
            }

        hashed_password = generate_password_hash(password)

        access_token = create_access_token(identity=email, fresh=True)

        user_model = User(firstName=firstName, lastName=lastName, username=username,
                          email=email, password=hashed_password)

        user_model.save()

        return {
            "message": "User created",
            "access_token": access_token,
            "user": user_model.to_json()
        }


class Me(Resource):
    @jwt_required()
    def get(self):
        user = User.objects(email=get_jwt_identity()).first()

        if user:
            return user.to_json()

        return {
            "message": "User not found"
        }
