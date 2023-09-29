from flask import Blueprint

bp = Blueprint('demo', __name__, template_folder='templates')

from . import views