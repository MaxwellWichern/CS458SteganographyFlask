from flask import Blueprint

bp = Blueprint('textSteg', __name__, template_folder='templates')

from . import views