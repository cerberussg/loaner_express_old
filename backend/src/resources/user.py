from flask_restful import Resource, reqparse
from src.models.user import UserModel
from flask_jwt import jwt_required, current_identity

class User(Resource):
    # pulls in request to parse
    parser = reqparse.RequestParser()
    # Set requirements for parser
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    parser.add_argument('site_location',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    parser.add_argument('admin',
        type=bool,
        required=False,
        help="This field cannot be empty"
    )
    parser.add_argument('super_user',
        type=bool,
        required=False,
        help="This field cannot be empty"
    )

    @jwt_required()
    # returns a user record by username
    def get(self, username):
        identity = current_identity
        if identity == None:
            return {"message": "You are not logged in"}, 400
        if identity.username != username:
            return {'message': "You are not authorized."}, 403

        user = UserModel.find_by_username(username)
        return user.json()

    @jwt_required()
    # inserts or updates records by username to database
    def put(self, username):
        # gets current identity (username, password, admin, super_user)
        identity = current_identity
        # loads json data and parses looking for args
        data = User.parser.parse_args()

        # existing user needed to query if a change being made to username already exists
        existing_user = UserModel.find_by_username(data['username'])

        # looks for current username passed in '/user/<name>' exists and if not create 
        user = UserModel.find_by_username(username)
        if identity.super_user == 0 and identity.username != username:
            return {'message': 'You are not authorized.'}, 403
        if user is None:
            user = UserModel(
                data['username'], 
                data['password'],
                data['site_location'],
                data['admin'],
                data['super_user'],
                identity.username
            )
        else:
            # it existed, now we must check a few other things to update a record
            # identity.username must match username being passed and existing user (username change, if any)
            if identity.super_user == 1 and existing_user is None:
                user.username = data['username']
                user.password = data['password']
                user.site_location = data['site_location']

                user.created_by = identity.username
            elif identity.username == username and existing_user is None:
                user.username = data['username']
                user.password = data['password']
                user.site_location = data['site_location']
                user.admin = user.admin
                user.super_user = user.super_user

                user.created_by = identity.username
            elif identity.username == existing_user.username:
                user.username = data['username']
                user.password = data['password']
                user.site_location = data['site_location']
                if identity.super_user == 1:
                    user.admin = data['admin']
                    user.super_user = data['super_user']
                else:
                    user.admin = user.admin
                    user.super_user = user.super_user
                
                user.created_by = identity.username
            else:
                return {'message': 'Username is already in use'}, 400
        
        user.save_to_db()

        return user.json()

class UserList(Resource):
    @jwt_required()
    # returns a list of all users
    def get(self):
        identity = current_identity
        if identity.super_user == 1:
            return {'users': [user.json() for user in UserModel.query.all()]}, 200
        else:
            return {'message': 'You are not authorized to view page'}, 403

class UserListBySite(Resource):
    @jwt_required()
    # returns list of users by site location
    def get(self, site_location):
        identity = current_identity
        if identity.super_user == 1:
            return {'users': [user.json() for user in UserModel.query.filter_by(site_location=site_location.lower()).all()]}, 200
        else:
            return { 'message': 'You are not authorized to view page'}, 403


class UserRegister(Resource):
    # pulls in request to parse
    parser = reqparse.RequestParser()
    # Set requirements for parser
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    parser.add_argument('site_location',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    
    # adds new user to the database
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        
        user = UserModel(
            data['username'].lower(), 
            data['password'], 
            data['site_location'].lower(),
            False,
            False,
            data.username.lower()
        )
        user.save_to_db()

        return {"messgae": "User created successfully."}, 201
        