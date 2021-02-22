from flask import Flask, render_template, session, redirect, request, url_for
from models.db import db
from flask_bootstrap import Bootstrap
from routes.register_route import register_route
from routes.detect_route import detect_route
from routes.training_route import training_route
from routes.user_route import user_route
import os
import shutil
import glob
from models.register import Register
from models.setting import Setting
from models.user import checkLogin
from routes.setting_route import setting_route
import random

app = Flask(__name__)
app.secret_key = "daxiong123zzzzzz"
Bootstrap(app)
app.register_blueprint(register_route)
app.register_blueprint(detect_route)
app.register_blueprint(training_route)
app.register_blueprint(user_route)
app.register_blueprint(setting_route)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Da123!@#@183.182.107.122:2020/face_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Da123!@#@localhost/face_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()


@app.before_request
def before_request_func():
    if str(request.url_rule) == '/domain':
        return render_template('domain.html')
    if checkLogin() == False:
        url = str(request.url_rule)
        if not url in '/login' and '/static/' not in request.path:
            return redirect(url_for('user_route.login'))


@app.route('/domain', methods=['POST', 'GET'])
def domain():
    return redirect('index')


@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect('index')


@app.route('/index', methods=['POST', 'GET'])
def index():
    # use for checking when deteted get data to display
    model_seeting = Setting.query.order_by(Setting.id.desc()).first()
    if model_seeting:
        session['generate_camera_id'] = model_seeting.camera_id
        session['number_of_times'] = model_seeting.number_of_times
        session['number_jitters'] = model_seeting.number_jitters
        session['accurate'] = 1 - ((model_seeting.accurate - 10) / 100)
        session['model_name'] = model_seeting.model_name

    else:
        model_seeting = Setting()
        model_seeting.camera_id = 0,
        model_seeting.number_of_times = 1,
        model_seeting.number_jitters = 1,
        model_seeting.accurate = 90,  # 90%
        model_seeting.model_name = 'HOG',
        db.session.add(model_seeting)
        db.session.commit()
        session['generate_camera_id'] = model_seeting.camera_id
        session['number_of_times'] = model_seeting.number_of_times
        session['number_jitters'] = model_seeting.number_jitters
        session['accurate'] = 1 - (model_seeting.accurate / 100)
        session['model_name'] = model_seeting.model_name
    """try:
        # session['generate_camera_id']
        setting = Setting.query.order_by(Setting.id.desc()).first()
        session['generate_camera_id'] = random.randint(000000, 999999)
    except:
        session['generate_camera_id'] = random.randint(000000, 999999)"""
    return render_template('index.html', camera='Camera', list_name='')


@app.route('/indexfull', methods=['POST', 'GET'])
def indexfull():
    return 'aaaaaaaaaaaa'


@app.route('/install', methods=['POST', 'GET'])
def install():
    return render_template('install.html')


@app.route('/cleanolddata', methods=['POST', 'GET'])
def cleanolddata():
    root = os.path.dirname(os.path.abspath(__file__))
    d = ['data', 'data_person', 'dataset_model', 'imgdataset']
    for dc in d:
        path = os.path.join(root, 'static', dc, '*')
        files = glob.glob(path)
        for f in files:
            try:
                shutil.rmtree(f)
            except:
                os.remove(f)
    if (request.args.get('id') == '0'):
        db.session.query(Register).delete()
        db.session.commit()
    return redirect('install')


@app.route('/jswebcam', methods=['POST', 'GET'])
def jswebcam():
    return render_template('js_webcam_copy.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False, ssl_context=('cert.pem', 'key.pem'), host='192.168.100.247',port='2020')
