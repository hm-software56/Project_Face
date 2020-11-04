from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint, send_file
from cameradetect import CameraDetect
from models.train import Traindata
from models.register import Register
from models.province import Provinces
from models.district import Districts
from models.village import Villages
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
webcam_id = 1
root = os.path.dirname(os.path.abspath(__file__))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detect_route.route('/capturepridict', methods=['GET', 'POST'])
def captureupload():
    if request.files.get('webcam'):
        file = request.files.get('webcam')
        filename = str(randint(1000000000, 9999999999)) + '.jpg'
        path = os.path.join('static', 'photo', 'detect')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        return render_template('predict.html')
    else:
        return jsonify(result=render_template('js_webcam.html'))


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
            break


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
            # pridectcamera.dropface(img)
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
    if len(pridectcamera.list_name_show) != session['list_persion_deteted']:
        session['list_persion_deteted'] = len(pridectcamera.list_name_show)
        person_ids = [];
        for person_id in pridectcamera.list_name_show:
            person_ids.append(person_id)
        model = Register.query \
            .join(Provinces, Provinces.id == Register.province_id) \
            .join(Districts, Districts.id == Register.district_id) \
            .join(Villages, Villages.id == Register.village_id) \
            .add_columns(Register.id, Register.code, Register.first_name, Register.last_name, Provinces.pro_name_la,
                         Districts.dis_name_la, Villages.vill_name_la) \
            .filter(Register.code.in_(person_ids)).all()
        print(len(model))
        return jsonify(
            result=render_template('persion_detail.html', model=model, list_person=pridectcamera.list_name_show))
    else:
        return 'No new Detetd new person'


@detect_route.route('/aa', methods=['GET'])
def aa():
    path = os.path.join(root, 'static', 'photos', 'detect', 'name')
    return path
