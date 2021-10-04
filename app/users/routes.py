from .forms import LoginForm, RegistrationForm
from . import users_bp
from flask import flash,render_template,abort,redirect,request,url_for,current_app
from app.models import User
from app import database
from sqlalchemy.exc import IntegrityError
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
