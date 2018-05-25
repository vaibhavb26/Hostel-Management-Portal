from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

class rate_record(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    rating_for = db.Column(db.String(80))
    rating_by = db.Column(db.String(80))
    rating = db.Column(db.Integer)

    def __init__(self,rating_for,rating_by,rating):
        self.rating = rating
        self.rating_for = rating_for
        self.rating_by = rating_by
    def __repr__(self):
        return '%r rated ' % self.rating_for