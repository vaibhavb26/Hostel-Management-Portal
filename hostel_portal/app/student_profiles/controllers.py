import re
from app import db
from app.admin_profiles.models import admin_requests
from app.login.models import User
from app.login.models import Admin
from app.complaints.models import Complaint
from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify,make_response,abort
from app.student_profiles.models import public_details
mod_stuProfile = Blueprint('mod_stuProfile',__name__,template_folder='templates',url_prefix='/student')

@mod_stuProfile.route('/home/<username>')
def view_home(username):
    if 'user_id' not in session or username!=session['user_id']: 
        return redirect('/login')
    else:
        student = User.query.filter_by(roll_no = int(username)).first()
        if student.status == 2:
            current_profile = public_details.query.filter_by(roll_no = int(username)).first()
            if current_profile.rate_count == 0:
                rating = 0
            else:
                rating = current_profile.rate_sum / current_profile.rate_count
            r =  make_response(render_template('index.html',students=User.query.all(),complaints = Complaint.query.all(),roll = username,rating = rating,total = public_details.query.all(),detail=public_details.query.filter_by(roll_no=username).first()))
            r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            return r    
        elif student.status == 0:
            return redirect(url_for('.view_form'))
        else:
            r = make_response(render_template('register_status1.html',email=student.email))
            r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            return r            
@mod_stuProfile.route('/notRegistered')
def view_form():
    if 'user_id' in session:
        roll_no = session['user_id']
        student = User.query.filter_by(roll_no = int(roll_no)).first()
        r =  make_response(render_template('register_page.html',email = student.email))
        r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return r    
    else:
        return redirect('/login')
@mod_stuProfile.route('/register', methods = ['POST'])
def add_change_status():
    name = request.form['name']
    rollNo = request.form['rollNo']
    email = request.form['email']
    hostel = request.form['hostel']
    room_no = request.form['roomNo']
    parents_name = request.form['parents_name']
    personal_no = request.form['personal_no']
    parents_no = request.form['parents_no']
    address = request.form['address']
    token = session.pop('_csrf_token',None)
    if not token or token!=request.form.get('_csrf_token'):
        return abort(403)
    student = User.query.filter_by(email = email).first()
    if student is None :
        flash('Invalid User')
        return redirect(url_for('.view_form'))
    elif student.roll_no != int(rollNo):
        flash('invalid credentials')
        return redirect(url_for('.view_form'))
    elif rollNo != session['user_id']:
        flash('Plese Dont register for others')
        return redirect(url_for('.view_form'))
    elif not re.match("^[a-zA-Z]*$",name):
    	flash('Invalid Name')
    	return redirect(url_for('.view_form'))
    elif not re.match("^[0-9]*$", room_no):
    	flash('Invalid Room No.')
    	return redirect(url_for('.view_form'))
    elif not re.match("^[a-zA-Z]*$", parents_name):
    	flash('Invalid parents name')
    	return redirect(url_for('.view_form'))
    elif not re.match("^[0-9]*$", personal_no):
    	flash('Invalid personal contact no.')
    	return redirect(url_for('.view_form'))
    elif not re.match("^[0-9]*$", parents_no):
    	flash('Invalid parents contact no.')
    	return redirect(url_for('.view_form'))
    else:
        student.status = 1
        add_student = admin_requests(name,rollNo,email,hostel,room_no,parents_name,personal_no,parents_no,address)
        db.session.add(add_student)
        db.session.commit()
        return redirect(url_for('.view_home',username = str(student.roll_no)))

@mod_stuProfile.route('/complaint')
def complaint():
    if 'user_id' not in session:
        return redirect('/login')
    r = make_response(render_template('complaint.html',complaints = Complaint.query.all(),User = User,Admin = Admin,public_details = public_details))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return r

@mod_stuProfile.route('/search', methods = ['POST'])
def search():
    searchval=request.form['searchvalue']
    query1=public_details.query.filter(public_details.name.like("%"+searchval+"%")).all()
    current_stu = public_details.query.filter_by(roll_no = int(session['user_id'])).first()
    for i in query1:
        if i==current_stu:
            query1.remove(current_stu)
    query2=public_details.query.filter(public_details.roll_no.like("%"+searchval+"%")).all()    
    for j in query2:
        if j==current_stu:
            query2.remove(current_stu)
    
    if searchval.isdigit()==True:
        r = make_response(render_template('search.html',requests = query2))
    else:
        r = make_response(render_template('search.html',requests = query1))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    if 'user_id' not in session:
        return redirect('/login')
    return r    
        
@mod_stuProfile.route('/details',methods=['POST'])
def detail():
    searchval1=request.form['detailval']
    student_search = public_details.query.filter_by(roll_no=searchval1).first()
    if student_search.rate_count == 0:
        rating = 0
    else:
        rating = student_search.rate_sum / student_search.rate_count 
    r = make_response(render_template('student_details.html',detail1=student_search,rating = rating))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return r        
@mod_stuProfile.route('/search1', methods = ['POST'])
def search1():
    searchval=request.form['q']
    query1=public_details.query.filter(public_details.name.like("%"+searchval+"%")).all()
    query2=public_details.query.filter(public_details.roll_no.like("%"+searchval+"%")).all()    
    if searchval.isdigit()==True:
        r = make_response(render_template('new_search.html',requests = query2))
    else:
        r = make_response(render_template('new_search.html',requests = query1))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return r    
@mod_stuProfile.route('/details1',methods=['POST'])
def detail1():
    searchval1=request.form['detailval1']
    r = make_response(render_template('new_details.html',detail1=public_details.query.filter_by(roll_no=searchval1).first()))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return r    