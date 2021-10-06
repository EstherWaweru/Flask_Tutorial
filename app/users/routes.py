from config import Config
from .forms import LoginForm, RegistrationForm
from . import users_bp
from flask import flash,render_template,abort,redirect,request,url_for,current_app
from app.models import User
from app import database,mail
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from flask_mail import Message
from main import celery
import time
################
#### routes ####
################

@users_bp.route('/')
def about():
    flash('Thanks for the site', 'info')
    return render_template('users/about.html', company_name = 'KarehTech')

@users_bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data,form.password.data)
                database.session.add(new_user)
                database.session.commit()
                flash('Thanks for registering!Please check your email to confirm your email address', 'success')
                #TODO: Send email activation link
                send.delay(form.email.data)
                return redirect(url_for('users.login'))
            except IntegrityError:
                database.session.rollback()
                flash(f'Email {form.email.data} already exists!','error')
        else:
            flash('Error in form data!', 'error')
    return render_template('users/register.html', form = form)

@users_bp.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            print("*********",user)
            if user and user.is_password_correct(form.password.data):
                print("-----------------")
                flash('Login succeeded','success')
                return redirect(url_for('users.about'))
        flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('users/login.html', form = form)

#generate confiration email
def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    confirm_url = url_for('users.confirm_email',token = confirm_serializer.dumps(user_email, salt = 'email-confirmation-salt'),
    _external=True)
    return Message(subject ='Kareh Tech confirm email',
    html = render_template('users/email_coonfirmation.html',confirm_url = confirm_url),recipients = [user_email])

#send email confirmation
@celery.task(name = 'celery_mail.send')
def send(email,is_retry = False):
     try:
        message = generate_confirmation_email(email)
        mail.send(message)
        return 'Mail sent successfully.'
     except Exception as e:
        print('==================================')
        print(f'Error: {e}')
        print('==================================')
        time.sleep(60) # Wait for a while, 1 minute tends to be a good measure as most configurations specify how many requests can be made a minute. 
        if not is_retry:  # Only retry once -> you could modify this to make the use of a counter.
            print('*****Attempting to send mail again...*****')
            send(email, is_retry=True) # Try again

@users_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = confirm_serializer.loads(token,salt = 'email-confirmation-salt',age = 3600)
    except BadSignature:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))
    
    user = User.query.filter_by(email = email).first()
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.email_confirmed = True
        database.session.add(user)
        database.session.commit()
        flash('Thank you for confirming your email address!', 'success')
    return redirect(url_for('users.about'))
    
        
        


