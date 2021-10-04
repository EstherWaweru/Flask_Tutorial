from . import database
from datetime import datetime
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

################
#### Models ####
################

class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer,primary_key = True)
    email = database.Column(database.String, unique = True)
    password = database.Column(database.String)
    created_at = database.Column(database.DateTime)
    email_confirmed = database.Column(database.Boolean, default = False)
    user_type = database.Column(database.String, default = 'User') #admin,superadmin

    def __init__(self, email: str, password: str, user_type = 'User'):
        """Create a new User object

        This constructor assumes that an email is sent to the new user to confirm
        their email address at the same time that the user is registered.
        """
        self.email = email
        self.password = generate_password_hash(password)
        self.user_type = user_type
        self.email_confirmed = False
        self.created_at = datetime.now()
    
    def is_password_correct(self, password: str):
        return check_password_hash(self.password,password)
 
    def __repr__(self):
        return f'User: {self.email}'
    
    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True
    
    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False
    
    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
    
    def is_admin(self):
        return self.user_type == 'Admin'
    
    def confirm_email_address(self):
        self.email_confirmed = True
    


        

