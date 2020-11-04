from models.db import db;
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, \
    DateField, TextAreaField
from flask import session, redirect
from flask_wtf import FlaskForm
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.String(255))
    type=db.Column(db.String(255))


class UserFrom(FlaskForm):
    username = StringField('ຊື່ເຂົ້າລະບົບ', validators=[validators.DataRequired()])
    password = PasswordField('ລະຫັດຜ່ານ', [validators.DataRequired()])
    status = SelectField('ສະຖານະ', choices=['1', '0'], validators=[validators.DataRequired()])
    type = SelectField('ປະເພດຜູ້ໃຊ້', choices=['Admin', 'Client'], validators=[validators.DataRequired()])


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


def checkLogin():
    if not session.get("login") is None:
        return True
        print('dddddddddddd')
    else:
        print('ssssssss')
        return False
