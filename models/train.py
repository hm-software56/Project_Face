import cv2
import os
import numpy as np
from PIL import Image
import pickle
import face_recognition
from numpy import asarray
from numpy import save, load
from models.register import Register
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
            model = Register.query.all()
            for register in model:
                person_codes.append(register.code)

            # person_ids = load('data_trained/news_dataset_ids.npy').tolist()

            for face_code in os.listdir(os.path.join('static', 'data')):
                if int(face_code) in person_codes:
                    print(face_code)
                    path = [os.path.join(os.path.join('static', 'data', face_code), f) for f in
                            os.listdir(os.path.join('static', 'data', face_code))]
                    for image in path:
                        try:
                            image_load = face_recognition.load_image_file(image)
                            image_encoding = face_recognition.face_encodings(image_load)[0]
                            known_face_encodings.append(image_encoding)
                            known_face_ids.append(face_code)
                        except:
                            os.remove(image)
                            # print(image)
                else:
                    print('No data set to train face_code match')
            if known_face_ids:
                save('data_trained/all_data_trainer_faces.npy', known_face_encodings)
                save('data_trained/all_data_trainer_ids.npy', known_face_ids)
                #save('data_trained/new_data_trainer_faces.npy', known_face_encodings)
                #save('data_trained/new_data_trainer_ids.npy', known_face_ids)

            """try:
                new_face_encodings = load('data_trained/new_data_trainer_faces.npy').tolist()
                new_face_ids = load('data_trained/new_data_trainer_ids.npy').tolist()

                face_encodings = load('data_trained/all_data_trainer_faces.npy').tolist()
                face_encodings = face_encodings + new_face_encodings
                face_ids = load('data_trained/all_data_trainer_ids.npy').tolist()
                face_ids = face_ids + new_face_ids

                save('data_trained/all_data_trainer_faces.npy', face_encodings)
                save('data_trained/all_data_trainer_ids.npy', face_ids)

                os.remove('data_trained/new_data_trainer_faces.npy')
                os.remove('data_trained/new_data_trainer_ids.npy')
                os.remove('data_trained/news_dataset_ids.npy')
            except:
                save('data_trained/all_data_trainer_faces.npy', known_face_encodings)
                save('data_trained/all_data_trainer_ids.npy', known_face_ids)

                os.remove('data_trained/new_data_trainer_faces.npy')
                os.remove('data_trained/new_data_trainer_ids.npy')
                os.remove('data_trained/news_dataset_ids.npy')"""
        except:
            print('No data set to train list in file')
        # return known_face_ids, known_face_encodings
