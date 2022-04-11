import email
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from src.models.user import User
from src.models.post import Post


class UserPosts(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str,
                            required=True, help="Body is required")
        args = parser.parse_args()

        content = args['content']

        current_user = get_jwt_identity()
        my_user = User.objects(email=current_user).first()

        if my_user:
            user_post = Post(content=content, creator=str(my_user._id))

            user_post.save()

            return {'message': user_post.to_json()}, 201

        return {
            'message': 'Post couldn\'t  created',
        }
