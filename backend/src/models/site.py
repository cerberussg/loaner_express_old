# -*- coding: utf-8 -*-
'''SiteModel

Purpose of the SiteModel is to handle functionality like;
saving to db, delete site out of db, find site by name, return site in JSON.

Besides inheriting the base Model class SiteModel has these DB fields:
name, loaners_on_site, loaners_issued

Author: Scott Goyette
Date: 03/14/2018
Email: scott_goyette@comcast.com, sgoyette@kerberosfoundation.com
'''

from .model import Model
from src.db import db

class SiteModel(Model, db.Model):
    '''SiteModel class 
    
    Inherits Model base class and db.Model.
    '''
    __tablename__ = 'sites'

    name = db.Column(db.String(80))
    loaners_on_site = db.Column(db.Integer)
    loaners_issued = db.Column(db.Integer)

    def __init__(self, name, loaners_on_site, loaners_issued, created_by):
        '''Mapping from DB to SiteModel object occurs in init.'''
        Model.__init__(self, created_by)
        self.name = name
        self.loaners_on_site = loaners_on_site
        self.loaners_issued = loaners_issued
    
    def save_to_db(self):
        '''Save to the DB.'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''Delete from the DB.'''
        db.session.delete(self)
        db.session.commit()

    def json(self):
        '''Returns site in JSON form.'''
        return {'name': self.name, 'loaners_on_site': self.loaners_on_site, 'loaners_issued': self.loaners_issued}

    @classmethod
    def site_by_name(cls, name):
        '''Returns site if found by name.'''
        return cls.query.filter_by(name=name).first()
