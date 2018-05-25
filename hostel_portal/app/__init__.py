# Import flask and template operators
from flask import Flask, render_template, session, jsonify
import random 
import string
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps

# Define the WSGI application object
app = Flask(__name__)

# Configurations

app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) 
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

from app.login.controllers import mod_login
from app.student_profiles.controllers import mod_stuProfile
from app.admin_profiles.controllers import mod_adProfile
from app.complaints.controllers import mod_complaint
from app.peer_rating.controllers import mod_ratePeer

app.register_blueprint(mod_login)
app.register_blueprint(mod_adProfile)
app.register_blueprint(mod_complaint)
app.register_blueprint(mod_stuProfile)
app.register_blueprint(mod_ratePeer)
# Define the database object which is imported
# by modules and controllers

db.create_all()

if __name__ == "__main__":
    app.run(host='127.0.0.1')
