from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify,make_response
from app.admin_profiles.models import admin_requests
from app import db
from app.student_profiles.models import public_details
from app.login.models import User
from app.login.models import Admin
from app.complaints.models import Complaint
mod_adProfile = Blueprint('mod_adProfile',__name__,template_folder='templates',url_prefix='/admin')

@mod_adProfile.route('/home/<username>')
def view_home(username):
    if 'user_id' not in session or username!=session['user_id']: 
        return redirect('/login')
    else:
        r = make_response(render_template('indexAd.html',requests = admin_requests.query.all(),email = session['user_id'],complaints=Complaint.query.all(),requestad=public_details.query.all()))
        r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return r
@mod_adProfile.route('/addUser',methods=['POST'])
def addUser():
    roll=request.form['roll']
    user=User.query.filter_by(roll_no=roll).first()
    user.status=2
    student=admin_requests.query.filter_by(roll_no=roll).first()
    name = student.name
    rollNo = student.roll_no
    email = student.email
    hostel = student.hostel
    room_no = student.room_no
    parents_name = student.parents_name
    personal_no = student.personal_no
    parents_no = student.parents_no
    address = student.address
    add_User = public_details(name,rollNo,email,hostel,room_no,parents_name,personal_no,parents_no,address)
    try:
        db.session.delete(student)
        db.session.commit()
        db.session.add(add_User)
        db.session.commit()
        resp={"success":"User added Successfully!"}
        response=jsonify(resp)
        return redirect(url_for('/admin/home',username=session['user_id']))

    except:
        db.session.rollback()
        resp={"error":"User couldn't be added!"}
        response=jsonify(resp)
        return redirect(url_for('/admin/home',username = session['user_id']))
@mod_adProfile.route('/delUser',methods=['POST'])
def delUser():
    roll=request.form['roll']
    user=User.query.filter_by(roll_no=roll).first()
    user.status=0
    student=admin_requests.query.filter_by(roll_no=roll).first()
    try:
        db.session.delete(student)
        db.session.commit()
        resp={"success":"removed"}
        response=jsonify(resp)
        return redirect(url_for('/admin/home',username = session['user_id']))    
    except:
        db.session.rollback()
        resp={"error":"couldn't be removed!"}
        response=jsonify(resp)
        return redirect(url_for('/admin/home',username = session['user_id']))        

@mod_adProfile.route('/details',methods=['POST'])    
def detail():
    searchval=request.form['detailval']
    stu = public_details.query.filter_by(roll_no=int(searchval)).first()
    if stu.rate_count == 0:
        rating = 0
    else:
        rating = stu.rate_sum / stu.rate_count
    r = make_response(render_template('stdetail.html',detail=public_details.query.filter_by(roll_no=searchval).first(),rating = rating))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    if 'user_id' not in session:
        return redirect('/login')
    return r
@mod_adProfile.route('/reg',methods=['POST'])    
def val():
    searchval=request.form['detailval1']
    r = make_response(render_template('streg.html',details=admin_requests.query.filter_by(roll_no=searchval).first()))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    if 'user_id' not in session:
        return redirect('/login')
    return r

@mod_adProfile.route('/search',methods=['POST'])
def search():
    searchval=request.form['searchvalue']
    query1=public_details.query.filter(public_details.name.like("%"+searchval+"%")).all()
    query2=public_details.query.filter(public_details.roll_no.like("%"+searchval+"%")).all()    
    if searchval.isdigit()==True:
        r = make_response(render_template('searchAd.html',requests = query2))
    else:        
        r = make_response(render_template('searchAd.html',requests = query1))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    if 'user_id' not in session:
        return redirect('/login')
    return r
@mod_adProfile.route('/complaint')
def complaint():
    r = make_response(render_template('complaintAd.html',complaints=Complaint.query.all(),User = User,Admin = Admin,public_details = public_details))
    r.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    if 'user_id' not in session:
        return redirect('/login')
    return r
