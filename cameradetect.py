from flask import session
import cv2
from PIL import ImageFont, ImageDraw, Image
import os
import pickle
import numpy as np
import face_recognition
import time
from models.train import Traindata
from autocrop import Cropper
from numpy import load
import random
# from flask_sqlalchemy import SQLAlchemy
from models.register import Register
import imutils
from collections import defaultdict

# db = SQLAlchemy()
root = os.path.dirname(os.path.abspath(__file__))

class CameraDetect(object):
    def __init__(self):
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.labels = {}
        self.labels_name = {}
        self.webcam_id = 0
        # addd new stylr
        self.face_locations = []
        self.face_encodings = []
        self.process_this_frame = True
        self.known_face_code = []
        self.known_face_encodings = []
        self.list_name_show = {}
        self.img_detect = ''
        self.chart=[];

        self.generate_camera_id = 0
        self.number_of_times = 1
        self.number_jitters = 1
        self.accurate = 0.35
        self.model_name = 'hog'
        self.xxx = 1

    def __del__(self):
        try:
            self.video.release()
        except:
            print('No Camera')

    def get_frame(self):
        if self.img_detect:
            path = os.path.join(root, 'static', 'photos', 'detect', self.img_detect)
            frame = cv2.imread(path)

            # Enable test manual images loop
            """print('==============================================')
            print('read===' + str(self.xxx))
            self.img_detect = str(self.xxx) + '.jpg'"""

        else:
            success, frame = self.video.read()
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        except:  # check camera if done have don't have return not found
            path = os.path.join(root, 'static', 'default', 'notfound_camera.png')
            frame = cv2.imread(path)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            # for rotate_img in [0, 90, 180, 270]:
            #    frame = imutils.rotate(frame, rotate_img)
            if self.model_name == 'hogcnn':  # Merge HOG and CNN Together
                models = ['hog', 'cnn']
            else:
                models = [self.model_name]
            self.face_locations.clear()
            face_location_count = 0
            for model in models:
                face_locations = face_recognition.face_locations(rgb_small_frame,
                                                                 number_of_times_to_upsample=self.number_of_times,
                                                                 model=model)
                face_location_count = len(face_locations)
                self.face_locations = self.face_locations + face_locations
                # self.face_locations = face_locations

            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations,
                                                                  num_jitters=self.number_jitters,
                                                                  model='large')
            # print(self.face_encodings)
            found_face = {}
            face_names = []
            count_face_found = len(self.face_encodings)
            # print(count_face_found)

            # Disable test manual images loop
            if count_face_found > 0:
                self.process_this_frame = False

            for face_encoding in self.face_encodings:
                count_face_found = count_face_found - 1
                preson_name = 'ບໍ່ຮູ້ຈັກຄົນນີ້.!'
                # distance_same_face = False
                # See if the face is a match for the known face(s)
                # tolerance=0.4 is distance_same_face
                # distans = [0.3, 0.4]
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding,
                                                         tolerance=self.accurate)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                # print(matches)
                best_match_index = np.argmin(face_distances)
                # print(best_match_index)
                # print(np.amin(face_distances))
                # print(best_match_index)
                # print(np.amin(face_distances))
                # print('loop ' + str(i))
                # print(matches[best_match_index])
                # print(self.known_face_code);exit()
                if matches[best_match_index]:  # and distance_same_face:
                    name_id = self.known_face_code[best_match_index]
                    # vl = str(np.amin(face_distances))
                    # preson_name = self.labels_name.get(int(name_id)) + " - " + vl[:4]
                    # list_p = {name_id: preson_name}
                    # list_p = {name_id: min(face_distances)}
                    # list_p.update(self.list_name_show)
                    # self.list_name_show = list_p

                    found_face.update({np.amin(face_distances): name_id})
                    # face_names.append(preson_name)

                else:
                    found_face.update(
                        {random.randint(1111111, 9999999): str(
                            random.randint(1111111, 9999999))})  # set values to unkwon
                    # face_names.append(preson_name)
            # print(self.list_name_show)

            # print('wwwwwwwwwwwwwwwwwwwwwwwwwwww')
            # print(found_face)
            res = defaultdict(list)
            for key, val in found_face.items():
                res[val].append(key)
            names = []
            i = 0
            for id, val in dict(res).items():
                i = i + 1
                if i <= face_location_count:
                    if len(str(id)) < 7:  # random id not found unknow person
                        # average = sum(val) / len(val)
                        # val = str(average)
                        # print(average)
                        val = str(min(val))
                        preson_name = self.labels_name.get(int(id)) + " - " + val[:4]
                        names.append(preson_name)
                        self.list_name_show.update({id: val})

                        self.chart.append(val)
                    else:
                        self.list_name_show.update({'0': 'ບໍ່ຮູ້ຈັກຄົນນີ້.!'})
                        names.append('ບໍ່ຮູ້ຈັກຄົນນີ້.!')
            # print(names)
            for (top, right, bottom, left), name in zip(self.face_locations, names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                font_size = 20
                # if len(models) == n:
                # Draw a box around the face
                if name != 'ບໍ່ຮູ້ຈັກຄົນນີ້.!':
                    cv2.rectangle(frame, (left, top), (right, bottom), (3, 128, 37), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (3, 128, 37), cv2.FILLED)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                label = name
                tex_color = '#FFFFFF'
                img = self.addlaotext(frame, left + 6, bottom - 30, label, tex_color, font_size)
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def loadLabelName(self):
        try:
            self.LoadModel()
            # get data full name from database
            face_code = self.known_face_code
            for code in np.unique(face_code):
                model = Register.query.filter_by(code=code).first()
                full_name = {model.code: model.first_name + " " + model.last_name}
                self.labels_name.update(full_name)

        except:
            print('Error name label')

    def addlaotext(self, image, x, y, label, tex_color, font_size):
        cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype('Phetsarath_OT.ttf', font_size)
        draw.text((x, y), label, font=font, fill=tex_color)
        return pil_im

    # load model trained and Code ID Face Set to Array
    def LoadModel(self):
        data_trainer_faces = load(os.path.join('static', 'dataset_model', 'all_data_trainer_faces.npy'))
        data_trainer_ids = load(os.path.join('static', 'dataset_model', 'all_data_trainer_ids.npy'))
        # self.known_face_code, self.known_face_encodings = Traindata().train()
        self.known_face_encodings = data_trainer_faces.tolist()
        self.known_face_code = data_trainer_ids.tolist()
        # print(type(self.known_face_encodings))

    def dropface(self, path):
        cropper = Cropper()
        cropped_array = cropper.crop(path)
        cropped_image = Image.fromarray(cropped_array)
        cropped_image.save(path)

    def SetParameters(self, generate_camera_id, number_of_times, number_jitters, model_name, accurate):
        if len(generate_camera_id) > 2:
            self.generate_camera_id = generate_camera_id
            self.webcam_id = generate_camera_id
        else:
            self.generate_camera_id = int(generate_camera_id)
            self.webcam_id = int(generate_camera_id)

        self.number_of_times = int(number_of_times)
        self.number_jitters = int(number_jitters)
        self.accurate = accurate
        self.model_name = model_name.lower()
