from urllib import request

from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint, send_file
from cameradetect import CameraDetect
from models.train import Traindata
from models.register import Register
from models.province import Provinces
from models.district import Districts
from models.village import Villages
from models.listfounddected import SaveFound, ListFound
import cv2, pafy
from random import choice
import time
from flask_bootstrap import Bootstrap
import os
import math
import shutil
from PIL import Image
from autocrop import Cropper
from random import randint
from numpy import load
from werkzeug.utils import secure_filename

detect_route = Blueprint('detect_route', __name__)
pridectcamera = CameraDetect()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
root = os.path.dirname(os.path.abspath(__file__))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detect_route.route('/capturepridict', methods=['GET', 'POST'])
def captureupload():
    if request.files.get('webcam'):
        file = request.files.get('webcam')
        filename = str(randint(1000000000, 9999999999)) + '.jpg'
        path = os.path.join('static', 'photos', 'detect')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        pridectcamera.img_detect = filename
        # file_stats = os.stat(os.path.join(path, filename))
        # print(file_stats.st_size)
        return jsonify(result=render_template('predict.html', time=time.time()))
    else:
        return jsonify(result=render_template('predict.html', time=time.time()))


@detect_route.route('/predict', methods=['GET', 'POST'])
def predict():
    pridectcamera.loadLabelName()
    pridectcamera.__del__()
    pridectcamera.process_this_frame = True
    if request.args.get('type') == 'img':
        return jsonify(result=render_template('modal_upload_detect.html'))
    elif request.args.get('type') == 'capture':
        return jsonify(result=render_template('modal_capture_detect.html'))
    else:
        if request.form.get('webcam_ip'):
            pridectcamera.__del__()
            if len(request.form.get('webcam_ip')) > 2:
                pridectcamera.webcam_id = request.form.get('webcam_ip')
            else:
                pridectcamera.webcam_id = int(request.form.get('webcam_ip'))
        pridectcamera.img_detect = ''
        return jsonify(result=render_template('predict.html', time=time.time()))


def genDetect(camera):
    # print(camera.webcam_id)
    url = str(camera.webcam_id)
    if "youtube" in url:
        video = pafy.new(camera.webcam_id)
        best = video.getbest(preftype="mp4")
        camera.webcam_id = best.url
    camera.video = cv2.VideoCapture(camera.webcam_id)
    s = 0
    while True:
        s = s + 1
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # Disable test manual images loop
        if camera.img_detect:
            break

        if s % 2 == 0:  # use cross one step fast then detect all
            camera.process_this_frame = True
        # print('xxxxxxxxxxxxxxxxxxxxx')


@detect_route.route('/video_detect', methods=['GET', 'POST'])
def video_detect():
    pridectcamera.SetParameters(session['generate_camera_id'], session['number_of_times'], session['number_jitters'],
                                session['model_name'], session['accurate'])

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
            frame = cv2.imread(img)
            height, width = frame.shape[:2]
            if height > 3500 or width > 3500:  # Big image must resizse
                frame = cv2.resize(frame, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
                cv2.imwrite(img, frame)

            print('No drop face use Oraginal')
        except:
            print('Errors No face drop')
        pridectcamera.img_detect = filename
        success = True

    if success:
        return jsonify(result=render_template('predict.html', time=time.time()))


@detect_route.route('/getdata', methods=['GET'])
def getdata():
    # pridectcamera.xxx = pridectcamera.xxx + 1  # enable test manual images loop
    if request.args.get('clear'):
        pridectcamera.list_name_show.clear()
    if pridectcamera.list_name_show:
        # print(pridectcamera.list_name_show)
        id = []
        for person_id, value in pridectcamera.list_name_show.items():
            id.append(person_id)
            SaveFound(person_id, session['generate_camera_id'], value, session['model_name'])
        # pridectcamera.list_name_show.clear()
        if pridectcamera.img_detect:
            try:
                os.remove(os.path.join('static', 'photos', 'detect', pridectcamera.img_detect))
            except:
                print('dont have remove img pridect.!')

        model = Register.query \
            .join(Provinces, Provinces.id == Register.province_id) \
            .join(Districts, Districts.id == Register.district_id) \
            .join(Villages, Villages.id == Register.village_id) \
            .join(ListFound, ListFound.person_id == Register.code) \
            .add_columns(Register.id, Register.code, Register.first_name, Register.last_name, Provinces.pro_name_la,
                         Districts.dis_name_la, Villages.vill_name_la, ListFound.camera_id, ListFound.camera_id) \
            .filter(ListFound.camera_id.in_([session['generate_camera_id']]), ListFound.person_id.in_(id)).order_by(
            ListFound.id.desc()).all()
        return jsonify(result=render_template('persion_detail.html', model=model))
    else:
        return 'No new Detetd new person'


@detect_route.route('/aa', methods=['GET'])
def aa():
    return jsonify(pridectcamera.chart)
