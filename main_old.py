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

app = Flask(__name__)
app.secret_key = "daxiong123"
Bootstrap(app)
setdatacamera = VideoCamera()
pridectcamera = CameraDetect()
root = os.path.dirname(os.path.abspath(__file__))
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
root = os.path.dirname(os.path.abspath(__file__))
webcam_id = 1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/jswebcam', methods=['POST', 'GET'])
def jswebcam():
    return render_template('js_webcam.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    setdatacamera.__del__()
    pridectcamera.__del__()
    pridectcamera.loadLabelName()
    form = Register()

    return render_template('index.html', form=form, camera='Camera', list_name=pridectcamera.labels_name)


def gen(camera):
    camera.video = cv2.VideoCapture(webcam_id)
    while True:
        check_face, frame = camera.get_frame()
        if check_face:
            camera.i = camera.i + 1
        if camera.i > 100:
            camera.__del__()
            path = os.path.join(root, 'static', 'photos', str(setdatacamera.person_id))
            try:
                shutil.rmtree(path)
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


@app.route('/video_feed', methods=['GET'])
def video_feed():
    pridectcamera.__del__()
    return Response(gen(setdatacamera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def genDetect(camera):
    camera.video = cv2.VideoCapture(webcam_id)
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_detect')
def video_detect():
    setdatacamera.__del__()
    return Response(genDetect(pridectcamera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/setdataset', methods=['POST', 'GET'])
def setdataset():
    if request.form.get('action'):
        setdatacamera.person_name = request.form.get('name')
        setdatacamera.person_id = setdatacamera.checkname()
        setdatacamera.savenewdatasetId(setdatacamera.person_id)
        setdatacamera.i = 0
        if request.form.get('action') == 'img':
            setdatacamera.webcam_or_img = True
            return jsonify(result=render_template('modal_upload.html'))
        else:
            setdatacamera.webcam_or_img = False
            return jsonify(result=render_template('setdataset.html', time=time.time()))
    else:
        return jsonify(result='wwwwwwwwwwwwwwwwwwwwwww')

@app.route('/jswebcamupload', methods=['GET', 'POST'])
def jswebcamupload():
    file = request.files.get('webcam')
    filename = str(randint(1000000000, 9999999999)) +'.jpg'
    path = os.path.join(root, 'static', 'photos','w')
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(os.path.join(path, filename))
    return 'Uploaded'
@app.route('/uploadfile', methods=['GET', 'POST'])
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
        path = os.path.join(root, 'static', 'photos', str(setdatacamera.person_id))
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        setdatacamera.drop(path, filename)
        success = True
    if success:
        return jsonify(result=render_template('setdataset.html', time=time.time()))


@app.route('/uploadfiledetect', methods=['GET', 'POST'])
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
        path = os.path.join(root, 'static', 'photos', 'detect')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        img = os.path.join(root, 'static', 'photos', 'detect', filename)
        # setdatacamera.drop(path, filename)
        try:
            #pridectcamera.dropface(img)
            print('No drop face')
        except:
            print('No face drop')
        pridectcamera.img_detect = filename
        success = True
    if success:
        return jsonify(result=render_template('predict.html', time=time.time()))


@app.route('/trainer')
def trainer():
    setdatacamera.__del__()
    pridectcamera.__del__()
    Traindata().train()
    return jsonify(result=render_template('trainer.html'))


@app.route('/predict')
def predict():
    pridectcamera.loadLabelName()
    if request.args.get('type') == 'img':
        return jsonify(result=render_template('modal_upload_detect.html'))
    else:
        pridectcamera.img_detect = ''
        return jsonify(result=render_template('predict.html', time=time.time()))


@app.route('/test')
def test():
    print(pridectcamera.LoadModel())
    # setdatacamera.checkname()
    return 'dddddd'


@app.route('/getdata', methods=['GET'])
def getdata():
    if request.args.get('clear'):
        pridectcamera.list_name_show.clear()
    return jsonify(
        result=render_template('persion_detail.html', list_person=pridectcamera.list_name_show))


@app.route('/file', methods=['GET', 'POST'])
def file():
    return render_template('file.html')


if __name__ == '__main__':
    app.run(debug=True)
