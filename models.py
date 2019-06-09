from flask import flash, session
from sqlalchemy.sql import func
from config import db, bcrypt, migrate

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    # Password requires 5-10 characters length, capital and lowercase letters, and special characters.
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{5,14}$')

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


class Ideas(db.Model):
    __tablename__ = "ideas"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    users_who_liked = db.relationship('Users', secondary=likes)
