from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators
from flask import session
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from autocrop import Cropper
from PIL import Image
import cv2
import os

db = SQLAlchemy()


class RegisterForm(Form):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])

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
                img = cv2.resize(gray[y:y + h+20, x:x + w+20], (200, 200))
                cv2.imwrite(os.path.join('static', 'data', str(session['regster_code']), filename), img)
            except:
                print('Error')


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    first_name = db.Column(db.String(500))
    last_name = db.Column(db.String(500))
