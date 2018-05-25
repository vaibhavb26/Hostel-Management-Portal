from flask_sqlalchemy import SQLAlchemy
from app import db

class answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    body = db.Column(db.Text)
    roll_no = db.Column(db.Integer)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'))
    complaint = db.relationship('Complaint',backref=db.backref('answers', lazy='dynamic'))
    def __init__(self,body,complaint,roll_no):
        self.body = body
        self.roll_no = roll_no
        self.complaint = complaint
    def __repr__(self):
        return '%r' % self.body

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    roll_no = db.Column(db.Integer)
    text = db.Column(db.Text)
    def __init__(self,text,roll_no):
        self.text = text
        self.roll_no = roll_no
    def __repr__(self):
        return '%r' % self.id
