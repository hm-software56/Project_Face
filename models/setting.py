from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, \
    DateField, TextAreaField
from flask import session
from flask_wtf import FlaskForm
from models.db import db


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.String(255))
    number_of_times = db.Column(db.Integer)
    number_jitters = db.Column(db.Integer)
    model_name = db.Column(db.String(255))


class SettingForm(FlaskForm):
    id = IntegerField('id')
    camera_id = StringField('ລະຫັດ/IP ກ້ອງ', [validators.DataRequired()])
    number_of_times = IntegerField('ຈໍານວນຄັ້ງຊອກໃບໜ້າ', [validators.DataRequired()])
    number_jitters = IntegerField('ຈໍານວນຄັ້ງວິເຄາະໃບໜ້າ', [validators.DataRequired()])
    # model_name = IntegerField('ຈໍານວນຄັ້ງວິເຄາະໃບໜ້າ', [validators.DataRequired()])
    model_name = SelectField('ວິທິການ (Model)', choices=[('HOG', 'HOG'), ('CNN', 'CNN'), ('HOGCNN', 'HOGCNN')],
                             validators=[validators.DataRequired()])
