from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, \
    DateField, TextAreaField
from flask import session
from flask_wtf import FlaskForm
from models.db import db
from autocrop import Cropper
from PIL import Image
import cv2
import os


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    first_name = db.Column(db.String(500))
    last_name = db.Column(db.String(500))
    province_id = db.Column(db.Integer)
    district_id = db.Column(db.Integer)
    village_id = db.Column(db.Integer)
    date_birth = db.Column(db.Date)
    card_id = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    expire_date = db.Column(db.Date)
    location_name = db.Column(db.String(255))
    section_name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    eduction = db.Column(db.String(255))
    other = db.Column(db.String(500))


class RegisterForm(FlaskForm):
    id = IntegerField('id')
    first_name = StringField('ຊື່', [validators.DataRequired()])
    last_name = StringField('ນາມສະກຸນ', [validators.DataRequired()])
    province_id = SelectField('ແຂວງ', choices=[], validators=[validators.DataRequired()])
    district_id = SelectField('ເມືອງ', choices=[], validators=[validators.DataRequired()])
    village_id = SelectField('ບ້ານ', choices=[], validators=[validators.DataRequired()])
    date_birth = DateField('ວັນເດືອນປິເກິດ', [validators.DataRequired()])
    card_id = StringField('ເລກບັດປະຈໍາຕົວ/ສໍາມະໂນຄົວ', [validators.DataRequired()])
    start_date = DateField('ອອກໃຫ້ວັນທີ່', [validators.DataRequired()])
    expire_date = DateField('ໝົດກໍານົດວັນທີ', [validators.DataRequired()])
    location_name = StringField('ສະຖານທີ່')
    section_name = StringField('ພາກສ່ວນ')
    position = StringField('ຕໍາແໜ່ງ')
    eduction = StringField('ລະດັບການສຶກສາ')
    other = TextAreaField('ລາຍລະອຽດອຶ່ນໆ')

    def dropface(self, filename):
        path = os.path.join('static', 'data', str(session['regster_code']), filename)
        image = cv2.imread(path)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image_img = image
        image = cv2.flip(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            try:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                img = cv2.resize(gray[y:y + h + 20, x:x + w + 20], (200, 200))
                cv2.imwrite(os.path.join('static', 'data', str(session['regster_code']), filename), img)
            except:
                print('Error')
