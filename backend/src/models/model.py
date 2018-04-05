# -*- coding: utf-8 -*-
'''Base Model Class

Handles basic functionality for all models.
DB connections, a few audit fields for auditing purposes.

Assigns base DB fields to other models:
id, created_at, updated_at, last_updated_by

Author: Scott Goyette
Date: 03/14/2018
Email: scott_goyette@comcast.com, sgoyette@kerberosfoundation.com
'''

from datetime import datetime

from src.db import db

class Model():
    '''Base Model class for all other models
    '''
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    last_updated_by = db.Column(db.String)

    def __init__(self, created_by):
        '''DB auditing variables are mapped during init.'''
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by
