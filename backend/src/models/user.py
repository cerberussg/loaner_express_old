# -*- coding: utf-8 -*-
'''UserModel

Purpose of the UserModel is to handle functionality like;
save to db, delete user from db, find user by name, return user in JSON.

Besides inheriting the base Model class UserModel has these DB fields:
username, password, site_location, admin, super_user

Author: Scott Goyette
Date: 03/14/2018
Email: scott_goyette@comcast.com, sgoyette@kerberosfoundation.com
'''

from .model import Model
from src.db import db

class UserModel(Model, db.Model):
    '''UserModel class 
    
    Inherits Model base class and db.Model.
    '''
    __tablename__ = 'users'

    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    site_location = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    super_user = db.Column(db.Boolean)

    def __init__(self, username, password, site_location, admin, super_user, created_by):
        '''Mapping from DB to UserModel object occurs in init.'''
        Model.__init__(self, created_by)
        self.username = username
        self.password = password
        self.site_location = site_location
        self.admin = admin
        self.super_user = super_user

    
    def save_to_db(self):
        '''Save user record to DB.'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''Delete user record from DB.'''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        '''Returns user if found by name'''
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        '''Returns user if found by ID.'''
        return cls.query.filter_by(id=_id).first()

    def json(self):
        '''Returns JSON object of user.'''
        return {'username': self.username, 'password': self.password, 
            'site_location': self.site_location, 'admin': self.admin, 
            'super_user': self.super_user}