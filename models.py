from flask import flash, session
from sqlalchemy.sql import func
from config import db, bcrypt, migrate

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    # Password requires 5-10 characters length, capital and lowercase letters, and special characters.
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{8,16}$')

likes = db.Table('likes', 
        db.Column('user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True),
        db.Column('idea_id', db.Integer,
        db.ForeignKey('ideas.id'), 
        primary_key=True))

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65))
    alias = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(255))
    liked_ideas = db.relationship('Ideas', secondary=likes)
    @classmethod
    def validate_registration(cls, user_info):
        is_valid = True
        if len(user_info['name']) < 1:
            is_valid = False
            flash('Please enter your name.', 'danger')
        if len(user_info['alias']) < 1:
            is_valid = False
            flash('Please enter an alias.', 'danger')
        elif len(user_info['alias']) > 0:
            for user in cls.query.all():
                if user.alias == user_info['alias']:
                    is_valid = False
                    flash('Alias already exists.', 'info')
        if len(user_info['email']) < 1:
            is_valid = False
            flash('Please enter an email address.', 'danger')
        elif not EMAIL_REGEX.match(user_info['email']):
            is_valid = False
            flash('Please enter a valid email address.', 'danger')
        elif EMAIL_REGEX.match(user_info['email']):
            for user in cls.query.all():
                if user.email == user_info['email']:
                    is_valid = False
                    flash('Email address already registered.', 'info')
        if len(user_info['pass']) < 1:
            is_valid = False
            flash('Please enter a password', 'danger')
        elif not PASSWORD_REGEX.match(user_info['pass']):
            is_valid = False
            flash('Password does not meet complexity requirements.', 'danger')
        elif user_info['pass'] != user_info['cpass']:
            is_valid = False
            flash('Passwords do not match.', 'danger')
        return is_valid
    @classmethod
    def validate_login(cls, user_info):
        is_valid = True
        match = 0
        if len(user_info['email']) < 1:
            is_valid=False
            flash("Please enter your email address.", "danger")
        elif len(user_info['pass']) < 1:
            is_valid=False
            flash("Please enter your password.", "danger")
        elif not EMAIL_REGEX.match(user_info['email']):
            is_valid=False
            flash("Please enter a valid email address.", "danger")
        else:
            for user in cls.query.all():
                if user.email == user_info['email']:
                    match += 1
                    this_user = user
                    session['userid'] = user.id
            if match < 1:
                is_valid=False
                flash("Email address is not registered.", "danger")
            elif match > 0:
                if not bcrypt.check_password_hash(this_user.password, user_info['pass']):
                    is_valid=False
                    flash("Incorrect username or password.", "danger")
        return is_valid
    @classmethod
    def register_user(cls, user_info):
        encrypted_pw = bcrypt.generate_password_hash(user_info['pass'])
        new_user = cls(name=user_info['name'], alias=user_info['alias'], email=user_info['email'], password=encrypted_pw)
        db.session.add(new_user)
        db.session.commit()
        for user in cls.query.all():
            if user.email == new_user.email:
                session['userid'] = user.id
        


class Ideas(db.Model):
    __tablename__ = "ideas"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users_who_liked = db.relationship('Users', secondary=likes)
    @classmethod
    def post_validation(cls, user_info):
        is_valid = True
        if len(user_info['idea']) < 1:
            is_valid = False
            flash("Please enter a post before submitting!", "danger")
        elif len(user_info['idea']) < 10:
            is_valid = False
            flash("Please enter at least 10 characters.", "danger")
        return is_valid
    @classmethod
    def add_post(cls, user_info):
        flash("Idea posted!", "success")
        new_post = cls(content=user_info['idea'], author=session['userid'])
        db.session.add(new_post)
        db.session.commit()