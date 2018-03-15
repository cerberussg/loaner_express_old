from flask_restful import Resource, reqparse
from src.models.user import UserModel
from flask_jwt import jwt_required, current_identity

class User(Resource):
    def get(self, name):
        identity = current_identity
        if identity.username != name:
            return {'message': "You are not authorized."}, 403

        user = UserModel.find_by_username(name)
        return user.json()


class UserList(Resource):
    jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}, 200