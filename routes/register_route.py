from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint
from camera import VideoCamera
import cv2
import time
import os
import shutil
from random import randint
from models.register import Register, RegisterForm
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

register_route = Blueprint('register_route', __name__)
setdatacamera = VideoCamera()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
webcam_id = 1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen(camera):
    camera.video = cv2.VideoCapture(webcam_id)
    while True:
        check_face, frame = camera.get_frame()
        if check_face:
            camera.i = camera.i + 1
        if camera.i > 100:
            camera.__del__()
            path = os.path.join('static', 'photos', str(setdatacamera.person_id))
            try:
                shutil.rmtree(path)  # use remove upload went dataset image done
            except:
                print('No path img remove')
            im = cv2.imread('static/default/done.jpg')
            res, im_png = cv2.imencode('.png', im)
            frame = im_png.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            break
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@register_route.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen(setdatacamera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@register_route.route('/setdataset', methods=['POST', 'GET'])
def setdataset():
    if request.form.get('action'):
        setdatacamera.person_name = request.form.get('name')
        setdatacamera.person_id = setdatacamera.checkname()
        setdatacamera.savenewdatasetId(setdatacamera.person_id)
        setdatacamera.i = 0
        if request.form.get('action') == 'img':  # use wind click choose images dataset
            setdatacamera.webcam_or_img = True
            return jsonify(result=render_template('modal_upload.html'))
        else:  # use when click camera capture dataset
            setdatacamera.webcam_or_img = False
            return jsonify(result=render_template('setdataset.html', time=time.time()))
    else:
        return jsonify(result='wwwwwwwwwwwwwwwwwwwwwww')


# Function upload dataset image when click poup process
@register_route.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    success = False
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join('static', 'data', str(session['regster_code']))
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        RegisterForm().dropface(filename)
        success = True
    if success:
        return jsonify(result=render_template('setdataset.html', time=time.time()))


# new function use javascript webcame


@register_route.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    model = Register.query.order_by(Register.id.desc()).first()
    if model:
        code = model.id + 1
    else:
        code = 1
    if form.validate_on_submit():
        insert = Register(
            first_name=form.data['first_name'],
            last_name=form.data['last_name'],
            code=code
        )
        db.session.add(insert)
        db.session.commit()
        session['regster_code'] = insert.code
        if (request.args.get('action') == 'camera'):
            return jsonify(result=render_template('modal_video_register.html'))
        else:
            return jsonify(result=render_template('modal_upload.html'))
    return render_template('register.html', form=form)


@register_route.route('/captureupload', methods=['GET', 'POST'])
def captureupload():
    file = request.files.get('webcam')
    filename = str(randint(1000000000, 9999999999)) + '.jpg'
    path = os.path.join('static', 'data', str(session['regster_code']))
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(os.path.join(path, filename))
    RegisterForm().dropface(filename)
    return 'Uploaded'
