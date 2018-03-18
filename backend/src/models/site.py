# coding=utf-8

from .model import Model
from src.db import db

class SiteModel(Model, db.model):
    __tablename__ = 'sites'

    name = db.Column(db.String(80))
    loaners_on_site = db.Column(db.Integer)
    loaners_issued = db.Column(db.Integer)

    def __init__(self, name, loaners_on_site, loaners_issued, created_by):
        Model.__init__(self, created_by)
        self.name = name
        self.loaners_on_site = loaners_on_site
        self.loaners_issued = loaners_issued
    
    # save_to_db, basic insert and update
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # return json object
    def json(self):
        return {'name': self.name, 'loaners_on_site': self.loaners_on_site, 'loaners_issued': self.loaners_issued}

    @classmethod
    # find site by name
    def site_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
