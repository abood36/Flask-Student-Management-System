from flask import Blueprint

students = Blueprint("students", __name__, template_folder="../templates/students")
from . import routes