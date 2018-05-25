from flask_sqlalchemy import SQLAlchemy
from app import db

class admin_requests(db.Model):
    name = db.Column(db.String(255))
    roll_no = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(255),unique = True)
    hostel = db.Column(db.String(255))
    room_no = db.Column(db.String(80))
    parents_name = db.Column(db.String(80))
    personal_no = db.Column(db.String(80))
    parents_no = db.Column(db.String(80))
    address = db.Column(db.String(1000))

    def __init__(self,name,roll_no,email,hostel,room_no,parents_name,personal_no,parents_no,address):
        self.name = name
        self.roll_no = roll_no
        self.room_no = room_no
        self.email = email
        self.hostel = hostel
        self.parents_name= parents_name
        self.personal_no = personal_no
        self.parents_no = parents_no
        self.address = address
    def __repr__(self):
        return 'request generated for %r' % self.roll_no    
