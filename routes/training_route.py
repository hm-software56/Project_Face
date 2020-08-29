from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, session, Blueprint
from camera import VideoCamera
from cameradetect import CameraDetect
from models.train import Traindata

training_route = Blueprint('training_route', __name__)

@training_route.route('/trainer')
def trainer():
    VideoCamera().__del__()
    CameraDetect().__del__()
    Traindata().train()
    return jsonify(result=render_template('trainer.html'))
