from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint
from camera import VideoCamera
from cameradetect import CameraDetect
from models.train import Traindata

training_route = Blueprint('training_route', __name__)
Train = Traindata()


@training_route.route('/trainer')
def trainer():
    VideoCamera().__del__()
    CameraDetect().__del__()
    Train.model_name = session['model_name'].lower()
    Train.train()
    return jsonify(result=render_template('trainer.html'))
