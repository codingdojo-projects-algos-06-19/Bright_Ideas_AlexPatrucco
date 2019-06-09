from flask import rendet_template, redirect, request, session
from config import db, migrate
from models import Users, Ideas

def index():
    return render_template("main.html")

