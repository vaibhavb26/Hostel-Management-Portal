from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify
from app import db
from app.complaints.models import Complaint
from app.complaints.models import answer
from app.login.models import Admin
mod_complaint = Blueprint('mod_complaint',__name__,url_prefix='/complaint')
@mod_complaint.route('/addComplaint',methods=['POST'])
def addComplaint():
    roll_no = session['user_id']
    text = request.form['text']
    complaint_new = Complaint(text,int(roll_no))
    db.session.add(complaint_new)
    db.session.commit()
    return redirect('/student/complaint')
	
@mod_complaint.route('/addAnswer',methods=['POST'])
def addAnswer():
    roll_no = session['user_id']
    text = request.form['answer_text']
    complaint_id = request.form['id']
    cobject = Complaint.query.filter_by(id=complaint_id).first()
    answer_new = answer(text,cobject,int(roll_no))
    db.session.add(answer_new)
    db.session.commit()
    return redirect('/student/complaint')
@mod_complaint.route('/addAnswerAd',methods=['POST'])
def addAnswerAd():
    username = session['user_id']
    adm = Admin.query.filter_by(email = username).first()
    roll_no = adm.serial_no
    text = request.form['answer_text']
    complaint_id = request.form['id']
    cobject = Complaint.query.filter_by(id=complaint_id).first()
    answer_new = answer(text,cobject,int(roll_no))
    db.session.add(answer_new)
    db.session.commit()
    return redirect('/admin/complaint')
