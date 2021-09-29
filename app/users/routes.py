from .forms import RegistrationForm
from . import users_bp
from flask import flash,render_template,abort,redirect,request,url_for,current_app
from app.models import User
from app import database
from sqlalchemy.exc import IntegrityError
################
#### routes ####
################

@users_bp.route('/about')
def about():
    flash('Thanks for the site', 'info')
    return render_template('users/about.html', company_name = 'KarehTech')

@users_bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data,form.email.password)
                database.session.add(new_user)
                database.session.commit()
                flash('Thanks for registering!Please check your email to confirm your email address', 'success')
                #TODO: Send email activation link
                return redirect(url_for('auth.login'))
            except IntegrityError:
                database.session.rollback()
                flash(f'Email {form.email.data} already exists!','error')
        else:
            flash('Error in form data!', 'error')
    return render_template('users/registration.html', form = form)
