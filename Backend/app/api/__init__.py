from flask import Blueprint

api = Blueprint('api', __name__)

from . import users
from . import images
from . import rt_structures
