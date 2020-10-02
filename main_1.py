from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session
from camera import VideoCamera
from cameradetect import CameraDetect
from models.train import Traindata
from models.register import Register
import cv2
from random import choice
import time
from flask_bootstrap import Bootstrap
import os
import shutil
from PIL import Image
from autocrop import Cropper
from random import randint
from numpy import load
from routes.register_route import register_route
from routes.detect_route import detect_route
from routes.training_route import training_route
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "daxiong123zzzzzz"
Bootstrap(app)
app.register_blueprint(register_route)
app.register_blueprint(detect_route)
app.register_blueprint(training_route)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Da123!@#@localhost/face_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

setdatacamera = VideoCamera()
pridectcamera = CameraDetect()


@app.route('/', methods=['POST', 'GET'])
def index():
    setdatacamera.__del__()
    pridectcamera.__del__()
    pridectcamera.loadLabelName()
    form = Register()

    return render_template('index.html', form=form, camera='Camera', list_name=pridectcamera.labels_name)


@app.route('/jswebcam', methods=['POST', 'GET'])
def jswebcam():
    return render_template('js_webcam.html')


@app.route('/testface', methods=['POST', 'GET'])
def testface():
    return render_template('modal_video_register.html')


@app.route('/jswebcamupload', methods=['GET', 'POST'])
def jswebcamupload():
    file = request.files.get('webcam')
    filename = str(randint(1000000000, 9999999999)) + '.jpg'
    path = os.path.join('static', 'photos', 'w')
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(os.path.join(path, filename))
    return 'Uploaded'


@app.route('/test')
def test():
    print(pridectcamera.LoadModel())
    # setdatacamera.checkname()
    return 'dddddd'


@app.route('/file', methods=['GET', 'POST'])
def file():
    return render_template('file.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, ssl_context='adhoc', host='192.168.50.112')
