import cv2
import os
import numpy as np
from PIL import Image
import pickle
import face_recognition
from numpy import asarray
from numpy import save, load
import cameradetect
import ast
import re

root = os.path.dirname(os.path.abspath(__file__))


class Traindata(object):

    def train(self):
        # data_trainer_faces = load('data_trained/data_trainer_faces.npy').tolist()
        # data_trainer_ids = load('data_trained/data_trainer_ids.npy').tolist()
        known_face_encodings = []
        known_face_ids = []
        try:
            person_ids = load('data_trained/news_dataset_ids.npy').tolist()
            for id in os.listdir(os.path.join(root, '..', 'static', 'data')):
                if int(id) in person_ids:
                    print(id)
                    path = [os.path.join(os.path.join(root, '..', 'static', 'data', id), f) for f in
                            os.listdir(os.path.join(root, '..', 'static', 'data', id))]
                    for image in path:
                        try:
                            image_load = face_recognition.load_image_file(image)
                            image_encoding = face_recognition.face_encodings(image_load)[0]
                            known_face_encodings.append(image_encoding)
                            known_face_ids.append(id)
                        except:
                            os.remove(image)
                            # print(image)
                else:
                    print('No data set to train id match')
            if known_face_ids:
                save('data_trained/new_data_trainer_faces.npy', known_face_encodings)
                save('data_trained/new_data_trainer_ids.npy', known_face_ids)

            try:
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
                os.remove('data_trained/news_dataset_ids.npy')
        except:
            print('No data set to train list in file')
        # return known_face_ids, known_face_encodings
