
from flask import Blueprint
users_bp = Blueprint('auth',__name__, template_folder = 'templates')
from . import routes