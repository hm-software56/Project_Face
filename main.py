from flask import Flask, render_template,session
from models.db import db
from flask_bootstrap import Bootstrap
from routes.register_route import register_route
from routes.detect_route import detect_route
from routes.training_route import training_route

app = Flask(__name__)
app.secret_key = "daxiong123zzzzzz"
Bootstrap(app)
app.register_blueprint(register_route)
app.register_blueprint(detect_route)
app.register_blueprint(training_route)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Da123!@#@localhost/face_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    session['list_persion_deteted'] = 0 # use for checking when deteted get data to display
    return render_template('index.html', camera='Camera', list_name='')


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, ssl_context='adhoc', host='192.168.43.114')
