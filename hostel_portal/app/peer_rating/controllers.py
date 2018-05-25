from flask import Flask,redirect,request,Blueprint,url_for,session,render_template
from app.student_profiles.models import public_details
from app.peer_rating.models import rate_record
from app import db
from app.login.models import User

mod_ratePeer = Blueprint('mod_ratePeer',__name__)
@mod_ratePeer.route('/rateStudent',methods = ['POST'])
def rate_student():
    rating = request.form['rating']
    rating_for = request.form['rating_for']
    rating_by = session['user_id']

    records = rate_record.query.filter_by(rating_for = rating_for).all()
    record = None
    for rate in records:
        if rate.rating_by == rating_by:
            record = rate
            break
    if record is None:
        record = rate_record(rating_for,rating_by,int(rating))
        db.session.add(record)
        rated_person = public_details.query.filter_by(roll_no = int(rating_for)).first()
        rated_person.rate_sum = rated_person.rate_sum + int(rating)
        rated_person.rate_count += 1
        db.session.commit()
    else:
        prev_rating = record.rating
        rated_person = public_details.query.filter_by(roll_no = int(rating_for)).first()
        rated_person.rate_sum -= prev_rating
        rated_person.rate_sum += int(rating)
        record.rating = int(rating)
        db.session.commit()
    rating1 = rated_person.rate_sum / rated_person.rate_count
    return render_template('student_details.html',detail1=rated_person,rating = rating1)

        
