from flask import render_template, redirect, request, session
from config import db, migrate
from models import Users, Ideas


# Login and Registration Page

def index():
    return render_template("main.html")

def register():
    is_valid = Users.validate_registration(request.form)
    if is_valid:
        Users.register_user(request.form)
        return redirect('/bright_ideas')
    else:
        return redirect('/')

def login():
    is_valid = Users.login_validation(request.form)
    if is_valid:
        return redirect('/bright_ideas')
    else:
        return redirect('/')

# Main User Console

def bright_ideas():
    if 'userid' in session:
        all_posts = Ideas.query.all()
        for user in Users.query.all():
            if user.id == session['userid']:
                current_user = user
        return render_template('bright_ideas.html', user=current_user, posts=all_posts)
    else:
        return redirect('/')

# Logout

def logout():
    session.clear()
    return redirect("/")