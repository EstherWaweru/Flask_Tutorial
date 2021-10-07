#send email confirmation
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from config import Config
from flask import render_template,url_for,current_app
from app import mail,celery
import time
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

#generate confiration email
def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    confirm_url = url_for('users.confirm_email',token = confirm_serializer.dumps(user_email, salt = 'email-confirmation-salt'),
    _external=True)
    return Message(subject ='Kareh Tech confirm email',
    html = render_template('users/email_coonfirmation.html',confirm_url = confirm_url),recipients = [user_email])