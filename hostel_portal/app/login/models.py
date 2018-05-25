from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    roll_no = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    status=db.Column(db.Integer)

    def __init__(self,roll_no,email,password,status):
        self.roll_no = roll_no
        self.email = email
        self.password = generate_password_hash(password)
        self.status=status
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<logged in as %r>' % self.email

class Admin(db.Model):
    serial_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))

    def __init__(self,email,password):
        self.email = email
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<logged in as %r>' % self.email
