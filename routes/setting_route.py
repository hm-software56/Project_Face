from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint, url_for
from models.db import db
from models.setting import Setting, SettingForm
from camera import VideoCamera
from cameradetect import CameraDetect

setting_route = Blueprint('setting_route', __name__)


@setting_route.route('/setting/', methods=['GET', 'POST'])
def setting():
    VideoCamera().__del__()
    CameraDetect().__del__()
    entry = Setting.query.order_by(Setting.id.desc()).first()
    if entry:
        form = SettingForm(obj=entry)
    else:
        form = SettingForm()
    if request.form:
        if request.form.get('id'):
            id = int(request.form.get('id'))
            model_seeting = Setting.query.get(id)
        else:
            model_seeting = Setting()
        model_seeting.camera_id = request.form.get('camera_id'),
        model_seeting.number_of_times = request.form.get('number_of_times'),
        model_seeting.number_jitters = request.form.get('number_jitters'),
        model_seeting.accurate = request.form.get('accurate'),
        model_seeting.model_name = request.form.get('model_name'),

        db.session.add(model_seeting)
        db.session.commit()
    return render_template('setting.html', form=form)
