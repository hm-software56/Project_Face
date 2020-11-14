import cv2
import os
import numpy as np
from PIL import Image
import pickle
import face_recognition
from numpy import asarray
from numpy import save, load
from models.register import Register
from shutil import copyfile
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
import cameradetect
import ast
import re


# root = os.path.dirname(os.path.abspath(__file__))


class Traindata(object):

    def train(self):
        # data_trainer_faces = load('data_trained/data_trainer_faces.npy').tolist()
        # data_trainer_ids = load('data_trained/data_trainer_ids.npy').tolist()
        known_face_encodings = []
        known_face_ids = []
        person_codes = []
        try:
            """model = Register.query.all()
            for register in model:
                person_codes.append(register.code)"""

            new_face_codes = load(os.path.join('static', 'dataset_model', 'new_face_ids.npy')).tolist()
            person_codes = new_face_codes

            for face_code in os.listdir(os.path.join('static', 'data')):
                if int(face_code) in person_codes:
                    i = 0
                    for file_name in os.listdir(os.path.join('static', 'data', face_code)):
                        self.dropface(face_code, file_name, i)

                    path = [os.path.join(os.path.join('static', 'data', face_code), f) for f in
                            os.listdir(os.path.join('static', 'data', face_code))]
                    for image in path:
                        try:
                            image_load = face_recognition.load_image_file(image)
                            image_encoding = face_recognition.face_encodings(image_load, num_jitters=4, model='large')[
                                0]
                            known_face_encodings.append(image_encoding)
                            known_face_ids.append(face_code)
                        except:
                            os.remove(image)
                            # print(image)
                else:
                    print('No data set to train face_code match')
            if known_face_ids:
                # save('data_trained/all_data_trainer_faces.h5', known_face_encodings)
                # save('data_trained/all_data_trainer_ids.h5', known_face_ids)
                save(os.path.join('static', 'dataset_model', 'new_data_trainer_faces.npy'), known_face_encodings)
                save(os.path.join('static', 'dataset_model', 'new_data_trainer_ids.npy'), known_face_ids)

            try:
                new_face_encodings = load(
                    os.path.join('static', 'dataset_model', 'new_data_trainer_faces.npy')).tolist()
                new_face_ids = load(os.path.join('static', 'dataset_model', 'new_data_trainer_ids.npy')).tolist()

                face_encodings = load(os.path.join('static', 'dataset_model', 'all_data_trainer_faces.npy')).tolist()
                face_encodings = face_encodings + new_face_encodings
                face_ids = load(os.path.join('static', 'dataset_model', 'all_data_trainer_ids.npy')).tolist()
                face_ids = face_ids + new_face_ids

                save(os.path.join('static', 'dataset_model', 'all_data_trainer_faces.npy'), face_encodings)
                save(os.path.join('static', 'dataset_model', 'all_data_trainer_ids.npy'), face_ids)

                os.remove(os.path.join('static', 'dataset_model', 'new_data_trainer_faces.npy'))
                os.remove(os.path.join('static', 'dataset_model', 'new_data_trainer_ids.npy'))
                os.remove(os.path.join('static', 'dataset_model', 'new_face_ids.npy'))
            except:
                save(os.path.join('static', 'dataset_model', 'all_data_trainer_faces.npy'), known_face_encodings)
                save(os.path.join('static', 'dataset_model', 'all_data_trainer_ids.npy'), known_face_ids)

                os.remove(os.path.join('static', 'dataset_model', 'new_data_trainer_faces.npy'))
                os.remove(os.path.join('static', 'dataset_model', 'new_data_trainer_ids.npy'))
                os.remove(os.path.join('static', 'dataset_model', 'new_face_ids.npy'))
        except:
            print('No data set to train list in file')
        # return known_face_ids, known_face_encodings

    def dropface(self, regster_code, filename, i):
        i = i + 1
        path = os.path.join('static', 'data', regster_code, filename)
        name_new = 'face_' + filename
        image = cv2.imread(path)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image = cv2.flip(image, 1)
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                if i == 1:  # Save first image when train use show when detete
                    path = os.path.join('static', 'data_person', regster_code)
                    if not os.path.exists(path):
                        os.makedirs(path)
                        cv2.imwrite(os.path.join('static', 'data_person', regster_code, '1.jpg'), image)
                try:
                    #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    img = cv2.resize(image[y:y + h + 20, x:x + w + 20], (200, 200))
                    cv2.imwrite(os.path.join('static', 'data', regster_code, name_new), img)
                    os.remove(os.path.join('static', 'data', regster_code, filename))
                except:
                    print('Error')
        else:
            if filename[0:4] != 'face':
                os.remove(os.path.join('static', 'data', regster_code, filename))
