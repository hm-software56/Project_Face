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
from models.user import checkLogin

app = Flask(__name__)
app.secret_key = "daxiong123zzzzzz"
Bootstrap(app)
app.register_blueprint(register_route)
app.register_blueprint(detect_route)
app.register_blueprint(training_route)
app.register_blueprint(user_route)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Da123!@#@localhost/face_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()


@app.before_request
def before_request_func():
    if checkLogin() == False:
        url = str(request.url_rule)
        if not url in '/login' and '/static/' not in request.path:
            return redirect(url_for('user_route.login'))

        # if request.script_root != "/static":
        #    print(request.script_root)


@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect('index')


@app.route('/index', methods=['POST', 'GET'])
def index():
    session['list_persion_deteted'] = 0  # use for checking when deteted get data to display
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
    d = ['data', 'data_person', 'dataset_model']
    for dc in d:
        path = os.path.join(root, 'static', dc, '*')
        files = glob.glob(path)
        for f in files:
            try:
                shutil.rmtree(f)
            except:
                os.remove(f)
    db.session.query(Register).delete()
    db.session.commit()
    return redirect('install')


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=False, ssl_context='adhoc', host='192.168.100.247',port='2020')
