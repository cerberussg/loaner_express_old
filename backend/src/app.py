# coding=utf-8

import datetime
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from src.security import authenticate, identity
from src.resources.user import User, UserList, UserRegister, UserListBySite
from src.resources.site import SiteList


# create Flask application
app = Flask(__name__)
CORS(app)
db_url = 'localhost:5433'
db_name = 'loaner_express'
db_user = 'postgres'
db_password = 'Krsn@_Das108'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Kl*0%Y4xd1_p960*'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Initialize jwt
app.config['JWT_AUTH_URL_RULE'] = '/login'
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

# declare endpoints

# user endpoints
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')
api.add_resource(UserListBySite, '/users/<string:site_location>')
api.add_resource(UserRegister, '/register')

# site endpoints
api.add_resource(SiteList, '/sites')

if __name__ != '__main__':
    from src.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)