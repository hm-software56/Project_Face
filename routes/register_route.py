from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint
from camera import VideoCamera
from cameradetect import CameraDetect
import cv2
import time
import os
import shutil
from random import randint
from models.db import db
from models.register import Register, RegisterForm
from numpy import save, load
from werkzeug.utils import secure_filename
from models.province import Provinces, ListProvince
from models.district import Districts, ListDistrictBy
from models.village import Villages, ListVillageBy
import glob

register_route = Blueprint('register_route', __name__)
setdatacamera = VideoCamera()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
webcam_id = 1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@register_route.route('/listregister', methods=['GET', 'POST'])
def listregister():
    models = Register.query \
        .join(Provinces, Provinces.id == Register.province_id) \
        .join(Districts, Districts.id == Register.district_id) \
        .join(Villages, Villages.id == Register.village_id) \
        .add_columns(Register.id, Register.code, Register.first_name, Register.last_name, Provinces.pro_name_la,
                     Districts.dis_name_la, Villages.vill_name_la, Register.card_id, Register.location_name,
                     Register.section_name) \
        .all()
    return render_template('listregister.html', models=models)


@register_route.route('/rview/', methods=['GET', 'POST'])
def rview():
    CameraDetect().__del__()  # Close camera background
    if request.args.get('id'):
        id = int(request.args.get('id'))
        entry = Register.query.get(id)
        form = RegisterForm(obj=entry)
        form.province_id.choices = ListProvince()
        form.district_id.choices = ListDistrictBy(entry.province_id)
        form.village_id.choices = ListVillageBy(entry.district_id)
        all_image = [(str(entry.code), f) for f in
                     os.listdir(os.path.join('static', 'data', str(entry.code)))]
    return render_template('register_view.html', form=form, all_image=all_image)


@register_route.route('/register/', methods=['GET', 'POST'])
def register():
    CameraDetect().__del__()  # Close camera background
    if request.args.get('id'):
        id = int(request.args.get('id'))
        entry = Register.query.get(id)
        form = RegisterForm(obj=entry)
        form.province_id.choices = ListProvince()
        form.district_id.choices = ListDistrictBy(entry.province_id)
        form.village_id.choices = ListVillageBy(entry.district_id)
    else:
        form = RegisterForm()
        model = Register.query.order_by(Register.id.desc()).first()
        if model:
            code = model.id + 1
            print(code)
        else:
            code = 1
        form.province_id.choices = ListProvince()
    if request.form:
        model_register = Register.query.filter_by(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            date_birth=request.form.get('date_birth')
        ).first()
        if model_register:
            code = model_register.code
        else:
            model_register = Register()
            code = code
            """insert = Register(
                first_name=request.form.get('first_name'),
                last_name=request.form.get('last_name'),
                code=code,
                province_id=request.form.get('province_id'),
                district_id=request.form.get('district_id'),
                village_id=request.form.get('village_id'),
                date_birth=request.form.get('date_birth'),
                card_id=request.form.get('card_id'),
                location_name=request.form.get('location_name'),
                section_name=request.form.get('section_name'),
                position=request.form.get('position'),
                eduction=request.form.get('eduction'),
                other=request.form.get('other'),
            )"""
        model_register.first_name = request.form.get('first_name'),
        model_register.last_name = request.form.get('last_name'),
        model_register.code = code,
        model_register.province_id = request.form.get('province_id'),
        model_register.district_id = request.form.get('district_id'),
        model_register.village_id = request.form.get('village_id'),
        model_register.date_birth = request.form.get('date_birth'),
        model_register.card_id = request.form.get('card_id'),
        model_register.location_name = request.form.get('location_name'),
        model_register.section_name = request.form.get('section_name'),
        model_register.position = request.form.get('position'),
        model_register.eduction = request.form.get('eduction'),
        model_register.other = request.form.get('other'),
        db.session.add(model_register)
        db.session.commit()

        session['regster_code'] = model_register.code
        Savenewfacecode(model_register.code)
        if (request.args.get('action') == 'camera'):
            return jsonify(result=render_template('modal_video_register.html'))
        else:
            return jsonify(result=render_template('modal_upload.html'))
    return render_template('register.html', form=form)


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
        # RegisterForm().dropface(filename)
        success = True
    if success:
        return jsonify(result=render_template('setdataset.html'))


# Create new ids dataset register new use when train
def Savenewfacecode(face_code):
    try:
        face_codes = load(os.path.join('static', 'dataset_model', 'new_face_ids.npy')).tolist()
        face_codes = face_codes + [face_code]
        save(os.path.join('static', 'dataset_model', 'new_face_ids.npy'), face_codes)
    except:
        save(os.path.join('static', 'dataset_model', 'new_face_ids.npy'), [face_code])


@register_route.route('/captureupload', methods=['GET', 'POST'])
def captureupload():
    file = request.files.get('webcam')
    filename = str(randint(1000000000, 9999999999)) + '.jpg'
    path = os.path.join('static', 'data', str(session['regster_code']))
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(os.path.join(path, filename))
    # RegisterForm().dropface(filename)
    return 'Uploaded'


@register_route.route('/listdistrict', methods=['GET', 'POST'])
def listdistrict():
    if request.form.get('province_id'):
        districts = Districts.query.filter_by(
            provinces_id=request.form.get('province_id')).all()
        option = '<option>=== ເລຶອກ ເມືອງ ===</option>'
        if districts:
            for district in districts:
                option = option + '<option value=' + str(district.id) + '>' + district.dis_name_la + '</option>'

    return option


@register_route.route('/listvillage', methods=['GET', 'POST'])
def listvillage():
    if request.form.get('district_id'):
        villages = Villages.query.filter_by(
            districts_id=request.form.get('district_id')).all()
        option = '<option>=== ເລຶອກ ບ້ານ ===</option>'
        if villages:
            for village in villages:
                option = option + '<option value=' + str(village.id) + '>' + village.vill_name_la + '</option>'

    return option


@register_route.route('/rdel', methods=['GET', 'POST'])
def rdel():
    if request.args.get('id'):
        id = request.args.get('id')
        reg = Register.query.filter_by(id=id).first()
        code = reg.code
        db.session.delete(reg)
        db.session.commit()
        root = os.path.dirname(os.path.abspath(__file__))
        d = ['data', 'data_person']
        for dc in d:
            path = os.path.join(root, '..', 'static', dc, str(code))
            try:
                shutil.rmtree(path)
            except:
                os.remove(path)
    return redirect('listregister')
