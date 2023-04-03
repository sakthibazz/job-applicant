from flask import Flask, render_template, redirect, url_for,request,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_paranoid import Paranoid

from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
import os
import time
port_app=9999
host_app="0.0.0.0"
#port_app=os.environ["JOB_PORT"]
#host_app=os.environ["JOB_HOST"]
from werkzeug import secure_filename

from random import *
# port_app=5000
# host_app="localhost"
import requests
import json 


app = Flask(__name__)
app.threaded=True
app.config['SECRET_KEY'] = 'Thisissupposedtobesecretasdadsasdadadadadadadaadaadadada!'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["JOB_DB"]
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://idia:postgres@postgres.cvc8b2isrkrv.us-west-2.rds.amazonaws.com/aroha_job_portal"
Bootstrap(app)
db = SQLAlchemy(app)


SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True

app.config['UPLOAD_FOLDER'] = "resumes"



def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)




class jobs(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(15000))
    industry = db.Column(db.String(50))
    functional_area = db.Column(db.String(80))
    skills = db.Column(db.String(800))
    seniority_level = db.Column(db.String(80))
    employment_type = db.Column(db.String(80))
    location_name = db.Column(db.String(80))
    company_name = db.Column(db.String(80))
    company_description = db.Column(db.String(8000))
    contact_email_address = db.Column(db.String(80))
    start_date= db.Column(db.String(80))
    end_date= db.Column(db.String(80))
    shcedule_date = db.Column(db.String(80))
    status=db.Column(db.String(80))
    user_id = db.Column(db.Integer)
    clientid = db.Column(db.String(50))


def __init__(self, title ,description ,industry ,functional_area ,skills ,seniority_level ,employment_type ,location_name ,company_name ,company_description ,contact_email_address ,start_date,end_date,shcedule_date ,status,user_id, clientid ):
   self.title = title
   self.description = description
   self.industry = industry
   self.functional_area = functional_area
   self.skills =  skills
   self.seniority_level = seniority_level
   self.employment_type = employment_type
   self.job_description = job_description
   self.company_description = company_description
   self.requirement = requirement
   self.contact_email_address = contact_email_address
   self.required_skills_for_job = required_skills_for_job
   self.status = status
   self.location_name = location_name
   self.company_name= company_name
   self.start_date = start_date
   self.end_date = end_date
   self.shcedule_date = shcedule_date
   self.user_id = user_id
   self.clientid = clientid




class applicant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    dob = db.Column(db.DateTime)
    yop = db.Column(db.String(80))

    email_id=db.Column(db.String(80))

    contact_no=db.Column(db.String(80))
    contact_no_alt=db.Column(db.String(80))
    university=db.Column(db.String(80))
    total_exp=db.Column(db.String(8))
    ref_name=db.Column(db.String(80))
    cover_letter=db.Column(db.String(8000))
    resume_name=db.Column(db.String(80))
    job_id = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)


def __init__(self, fullname, dob, yop, email_id, contact_no, contact_no_alt, university, total_exp, ref_name, cover_letter, job_id, pub_date  ):
   self.fullname = fullname
   self.dob = dob
   self.yop = yop
   self.email_id = email_id
   self.contact_no =  contact_no
   self.contact_no_alt = contact_no_alt
   self.university = university
   self.total_exp = total_exp
   self.ref_name = ref_name
   self.cover_letter = cover_letter
   self.resume_name = resume_name
   self.job_id=job_id
   self.pub_date=pub_date




class news_letter_subscription(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_letter_sub_email = db.Column(db.String(150))
    
    

def __init__(self, news_letter_sub_email ):
   self.news_letter_sub_email = news_letter_sub_email



class job_alert_subscription(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_alert_sub_email = db.Column(db.String(150))
    
    

def __init__(self, news_letter_sub_email ):
   self.job_alert_sub_email = job_alert_sub_email






@app.route('/aa', methods=['GET', 'POST'])

@nocache
def job_searcha():

  return render_template('worker_search.html')






@app.route('/', methods=['GET', 'POST'])

@nocache
def job_search():

  return render_template('job_search.html',data = jobs.query.filter(jobs.status=="checked").all())




@app.route('/job_details', methods=['GET', 'POST'])

@nocache
def job_details():

  job_id=request.form["job_id"].strip()
  print job_id
  

  return render_template('job_details.html',data=jobs.query.filter(jobs.id == job_id).first())


@app.route('/apply', methods=['GET', 'POST'])

@nocache
def apply():
  if request.method == 'POST':
    fn=request.form['name']

    dob = request.form['dob']

    yop = request.form['yop']

    email = request.form['email']

    tel1 = request.form['tel1']

    tel2 = request.form['tel2']

    u_name=request.form['u_name']

    exp= request.form['exp']

    ref_name=request.form['ref_name']

    mes = request.form['message']

    job_id = request.form['job_id']



    url = "http://itap.aroha.co.in/api00120001200011030040030004030302030000302"
    f = request.files['file']
    filename=(f.filename).split('.')
    filename=fn+str(randint(1,99999))+'.'+filename[1]
    
    meta={'fullname':fn, 'dob':dob, 'yop':yop, 'email_id':email,  'contact_no':tel1, 'contact_no_alt':tel2, 'university':u_name, 'total_exp':exp,'ref_name':ref_name, 'cover_letter':mes, 'resume_name':filename, 'job_id':job_id}
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
    r = requests.post(url, files={'file': open((os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))), 'rb'),'json': (json.dumps(meta),'application/json')} )
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
    if r.text=="False":
      flash(u'We already have your profile, we will get back to you, if we find matching jobs.', 'alert-danger')
      return render_template('job_details.html',data=jobs.query.filter(jobs.id == job_id).first())

    
    print 'file saveda as'+filename

    new_applicant = applicant(fullname=fn, dob=dob, yop=yop, email_id=email,  contact_no=tel1, contact_no_alt=tel2, university=u_name, total_exp=exp, ref_name=ref_name, cover_letter=mes, resume_name=filename, job_id=job_id)
    db.session.add(new_applicant)
    db.session.commit()

  
  flash(u'Thank you for submitting your resume we will contact you soon as possible .', 'alert-success')

  return render_template('job_details.html',data=jobs.query.filter(jobs.id == job_id).first())



@app.route('/subscription', methods=['GET', 'POST'])

@nocache
def subscription():
  if request.method == 'POST':
    
    email_sub = request.form['email']

    subscriber = job_alert_subscription(job_alert_sub_email=email_sub  )
    db.session.add(subscriber)
    db.session.commit()

  
  flash(u"thank you for your subscription to Aroha's Job Portal.", 'alert-success')

  return redirect(url_for("job_search"))





if __name__ == '__main__':
    app.run(
        host=host_app,
        port=port_app,
        # threaded=True,
        debug=True
        
        

       
    )
