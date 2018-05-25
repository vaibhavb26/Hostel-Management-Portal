from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify,make_response,abort
from app.login.models import User
from app.login.models import Admin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

mod_login = Blueprint('mod_login',__name__,template_folder='templates')
@mod_login.route('/')
def redirect_to():
    if 'user_id' in session:
        if session['type'] == "student":
            return redirect(url_for('mod_stuProfile.view_home',username=session['user_id']))
        else:
            return redirect(url_for('mod_adProfile.view_home',username=session['user_id']))    
    else:
        return redirect('/login')
@mod_login.route('/login/')
def check_session():
    r = make_response(render_template('index_login.html'))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    if 'user_id' in session:
        if session['type'] == "student":
            return redirect(url_for('mod_stuProfile.view_home',username=session['user_id']))
        else:
            return redirect(url_for('mod_adProfile.view_home',username=session['user_id']))    
    else:
        return r

@mod_login.route('/validate', methods=['POST'])
def login():
    if 'user_id' in session:
        if session['type'] == "student":
            return redirect(url_for('mod_stuProfile.view_home',username=session['user_id']))
        else:
            return redirect(url_for('mod_adProfile.view_home',username=session['user_id']))    
    else:
        username = request.form['username']
        password = request.form['password']
        token = session.pop('_csrf_token',None)
        user = User.query.filter_by(email = username).first()
        if not token or token!= request.form.get('_csrf_token'):
            return abort(403)
        else: 
            if  user and user.check_password(password)==True:
                session['user_id'] = str(user.roll_no)
                session['type'] = "student"
                return redirect(url_for('mod_stuProfile.view_home',username=str(user.roll_no)))    
            else:
                flash('Invalid credentials')
                r =  make_response(render_template('index_login.html',scroll = "login"))
                r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                return r  

@mod_login.route('/validateAd', methods=['POST'])
def loginAd():
    username = request.form['username']
    password = request.form['password']
    admin = Admin.query.filter_by(email = username).first()
    token = session.pop('_csrf_token',None)    
    if not token or token!= request.form.get('_csrf_token'):
        return abort(403)
    else:
        if  admin and admin.check_password(password)==True:
            session['user_id'] = username
            session['type'] = "admin"
            return redirect(url_for('mod_adProfile.view_home',username=username))    
        else:
            flash('Invalid credentials')
            return render_template('index_login.html',scroll = "login")  

@mod_login.route('/create',methods=['POST'])
def create_user():
    roll_no=request.values.get("roll_no")
    email=request.values.get("email")
    password=request.values.get("password")
    status=request.values.get("status")
    user=User(roll_no,email,password,status)
    try:
        db.session.add(user)
        db.session.commit()
        resp={"success":"User added successfully!"}
        return jsonify(resp)
    except:
        db.session.rollback()
        resp={"error":"User couldn't be  added"}
        return jsonify(resp)

@mod_login.route('/createAd',methods=['POST'])
def create_admin():
    email=request.values.get("email")
    password=request.values.get("password")
    admin=Admin(email,password)
    try:
        db.session.add(admin)
        db.session.commit()
        resp={"success":"Admin added successfully!"}
        return jsonify(resp)
    except:
        db.session.rollback()
        resp={"error":"Admin couldn't be  added"}
        return jsonify(resp)

@mod_login.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('type',None)
    return redirect('/login')
