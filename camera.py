from flask import Flask, session, redirect, url_for, escape, request
import cv2
import numpy as np
import requests
import os
import time
import pickle
from numpy import save, load
from random import choice
from PIL import Image
from autocrop import Cropper

root = os.path.dirname(os.path.abspath(__file__))


class VideoCamera(object):
    def __init__(self):
        self.video = ''
        self.i = 0
        self.offset = 0
        self.person_name = ''
        self.person_id = ''
        self.first_capture = True
        self.webcam_or_img = False

    def __del__(self):
        try:
            self.video.release()
        except:
            print('No Camera')

    def get_frame(self):
        # success, image = self.video.read()
        if self.webcam_or_img:
            path = os.listdir(os.path.join(root, 'static', 'photos', str(self.person_id)))
            try:
                image = cv2.imread(os.path.join(root, 'static', 'photos', str(self.person_id), path[self.i]))
            except:
                image = cv2.imread(os.path.join(root, 'static', 'photos', str(self.person_id), choice(path)))
        else:
            success, image = self.video.read()
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image_img = image
        image = cv2.flip(image, 1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        check_face = False
        for (x, y, w, h) in faces:
            check_face = True
            path = "static/data/" + str(self.person_id)
            path_img = "static/data_person/" + str(self.person_id)  # use for save img display list home page
            if not os.path.exists(path):
                os.makedirs(path)
                os.makedirs(path_img)
            try:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                img = cv2.resize(gray[y:y + h, x:x + w], (130, 100))
                # cv2.imwrite(path + "/" + str(time.time()) + ".jpg", image)
                if self.first_capture:
                    self.first_capture = False
                    cv2.imwrite(path_img + "/1.jpg", image_img)
                    self.dropface(path_img + "/1.jpg")
                else:
                    cv2.imwrite(path + "/" + str(time.time()) + ".jpg", img)
            except:
                print('Error')
        ret, jpeg = cv2.imencode('.jpg', image)
        return check_face, jpeg.tobytes()

    def checkname(self):
        try:
            with open("data_trained/name_labels.pickle", "rb") as f:
                labels_ = pickle.load(f)
                print(labels_)
                labels = {k: v for k, v in labels_.items()}
                person_id = None
                for k, v in labels_.items():
                    if v == self.person_name:
                        person_id = k
                        break

                if person_id is None:
                    person_id = len(labels) + 1
                    labels[person_id] = self.person_name
                    self.savename(labels)
        except:
            person_id = 1
            labels = {}
            labels[person_id] = self.person_name
            self.savename(labels)
        return person_id

    def savename(self, labels):
        with open("data_trained/name_labels.pickle", "wb") as f:
            pickle.dump(labels, f)

    def savenewdatasetId(self, person_id):
        ids = [person_id]
        try:
            person_ids = load('data_trained/news_dataset_ids.npy').tolist()
            person_ids.append(person_id)
            ids = list(set(person_ids))
        except:
            print('No file new data set')
        save('data_trained/news_dataset_ids.npy', ids)
        # print(ids)

    def drop(self, path, img):
        image = Image.open(os.path.join(path, img))
        width = image.size[0]
        height = image.size[1]
        aspect = width / float(height)
        ideal_width = 400
        ideal_height = 400
        ideal_aspect = ideal_width / float(ideal_height)
        if aspect > ideal_aspect:
            # Then crop the left and right edges:
            new_width = int(ideal_aspect * height)
            offset = (width - new_width) / 2
            resize = (offset, 0, width - offset, height)
        else:
            # ... crop the top and bottom:
            new_height = int(width / ideal_aspect)
            offset = (height - new_height) / 2
            resize = (0, offset, width, height - offset)

        thumb = image.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
        thumb.save(os.path.join(path, img))

    def dropface(self, path):
        cropper = Cropper()
        cropped_array = cropper.crop(path)
        cropped_image = Image.fromarray(cropped_array)
        cropped_image.save(path)
