# coding=utf-8

from .model import Model
from src.db import db

class SiteModel(Model, db.model):
    __tablename__ = 'sites'

    