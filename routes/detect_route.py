from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint
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
from werkzeug.utils import secure_filename

detect_route = Blueprint('detect_route', __name__)
pridectcamera = CameraDetect()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
webcam_id = 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detect_route.route('/predict')
def predict():
    pridectcamera.loadLabelName()
    if request.args.get('type') == 'img':
        return jsonify(result=render_template('modal_upload_detect.html'))
    else:
        pridectcamera.img_detect = ''
        return jsonify(result=render_template('predict.html', time=time.time()))


def genDetect(camera):
    camera.video = cv2.VideoCapture(webcam_id)
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if camera.img_detect:
            exit()


@detect_route.route('/video_detect')
def video_detect():
    return Response(genDetect(pridectcamera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@detect_route.route('/uploadfiledetect', methods=['GET', 'POST'])
def uploadfiledetect():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    success = False
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join('static', 'photos', 'detect')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        img = os.path.join('static', 'photos', 'detect', filename)
        # setdatacamera.drop(path, filename)
        try:
            #pridectcamera.dropface(img)
            print('No drop face use Oraginal')
        except:
            print('Errors No face drop')
        pridectcamera.img_detect = filename
        success = True
    if success:
        return jsonify(result=render_template('predict.html', time=time.time()))


@detect_route.route('/getdata', methods=['GET'])
def getdata():
    if request.args.get('clear'):
        pridectcamera.list_name_show.clear()
    return jsonify(
        result=render_template('persion_detail.html', list_person=pridectcamera.list_name_show))
