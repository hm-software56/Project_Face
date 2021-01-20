from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint, url_for
from models.db import db
from models.user import User, UserFrom, encrypt_password, check_encrypted_password

user_route = Blueprint('user_route', __name__)


@user_route.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@user_route.route('/login', methods=['GET', 'POST'])
def login():
    # a = encrypt_password('Da123!@#')
    # print(check_encrypted_password('Da123!@#qq', a))
    form = UserFrom()
    if request.form.get('username'):
        login = User.query.filter_by(
            username=request.form.get('username'),
            # password=request.form.get('password'),
            status='1'
        ).first()
        if login:
            if check_encrypted_password(request.form.get('password'), login.password):
                session['login'] = {'id': login.id, 'username': login.username, 'type': login.type}
                return redirect('/')
    return render_template('login.html', form=form)


@user_route.route('/user', methods=['GET', 'POST'])
def user():
    a = encrypt_password('12345')
    print(a)
    # print(check_encrypted_password('Da123!@#qq', a))

    return a
