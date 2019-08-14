"""
models.py
-------------
*User, Password and Access Models*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"""

from flask import Flask, render_template, request, session, redirect, jsonify
from config import Conf
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager,login_user, logout_user, login_required
from sqlalchemy import func, create_engine

app = Flask(__name__)
app.config.from_object(Conf)
db = SQLAlchemy(app)

class Auth_User(db.Model, UserMixin):
    __tablename__ = 'authorizer_user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    token = db.Column(db.String(1000))
    note =  db.Column(db.String(1000))

    def get_id(self):
        """
        :return: self.user_id
        """
        return self.user_id

    def is_authenticated(self):
        """
        :return: True
        """
        return True

    def is_active(self):
        """
        :return: True
        """
        return True

    def is_anonymous(self):
        """
        :return: False
        """
        return False


class Auth_Pass(db.Model):
    __tablename__ = 'authorizer_password'
    pass_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    note =  db.Column(db.String(1000))
    host =  db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('authorizer_user.user_id'))
    userref = db.relationship('Auth_User', backref='authorizer_password')


class Auth_Access(db.Model):
    __tablename__ = 'authorizer_access'
    access_id = db.Column(db.Integer, primary_key=True)
    pass_id = db.Column(db.Integer, db.ForeignKey('authorizer_password.pass_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('authorizer_user.user_id'))

    passref = db.relationship('Auth_Pass', backref = 'authorizer_access')
    userref = db.relationship('Auth_User', backref = 'authorizer_access')
