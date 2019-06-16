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
    is_valid = Users.validate_login(request.form)
    if is_valid:
        return redirect('/bright_ideas')
    else:
        return redirect('/')

# Main User Console

def bright_ideas():
    if 'userid' in session:
        all_posts = Ideas.query.all()
        all_users = Users.query.all()
        for user in all_users:
            if user.id == session['userid']:
                current_user = user
            else:
                continue
        return render_template('bright_ideas.html', user=current_user, all_users=all_users, posts=all_posts)
    else:
        return redirect('/')

def post_idea():
    if 'userid' in session:
        is_valid = Ideas.post_validation(request.form)
        if is_valid:
            Ideas.add_post(request.form)
    return redirect('/bright_ideas')

def like(id):
    if 'userid' in session:
        Ideas.like(id)
        return redirect('/bright_ideas')
    else:
        return redirect('/')

# User Profile

def user_view(id):
    if 'userid' in session:
        post_count = 0
        all_users = Users.query.all()
        all_posts = Ideas.query.all()
        for user in all_users:
            if user.id == int(id):
                current_user = user
            else:
                continue
        for post in all_posts:
            if post.author == int(id):
                post_count += 1
        return render_template('user_view.html', user=current_user, all_posts=all_posts, all_users=all_users, user_posts=post_count)
    else:
        return redirect('/')


# Logout

def logout():
    session.clear()
    return redirect("/")