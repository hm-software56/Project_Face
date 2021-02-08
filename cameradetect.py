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

        self.generate_camera_id = 0
        self.number_of_times = 1
        self.number_jitters = 1
        self.model_name = 'hog'

    def __del__(self):
        try:
            self.video.release()
        except:
            print('No Camera')

    def get_frame(self):
        if self.img_detect:
            path = os.path.join(root, 'static', 'photos', 'detect', self.img_detect)
            frame = cv2.imread(path)
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
        face_names = []
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            # for rotate_img in [0, 90, 180, 270]:
            #    frame = imutils.rotate(frame, rotate_img)
            self.face_locations = face_recognition.face_locations(rgb_small_frame,
                                                                  number_of_times_to_upsample=self.number_of_times,
                                                                  model=self.model_name)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations,
                                                                  num_jitters=self.number_jitters,
                                                                  model='large')
            found_face = {}
            count_face_found = len(self.face_encodings)
            if count_face_found > 0:
                self.process_this_frame = False

            for face_encoding in self.face_encodings:
                count_face_found = count_face_found - 1
                preson_name = 'ບໍ່ຮູ້ຈັກຄົນນີ້.!'
                # distance_same_face = False
                # See if the face is a match for the known face(s)
                # tolerance=0.4 is distance_same_face
                distans = [0.3, 0.4]
                for dst in distans:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=dst)
                    if True in matches:
                        break
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                """j = np.array(face_distances)
                face_distance_lessthen = np.sort(j[j < 0.1])  #
                if face_distance_lessthen.all():
                    distance_same_face = True"""
                """for i, face_distance in enumerate(face_distances):
                    # print(i)
                    # print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
                    # print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(
                    #    face_distance < 0.6))
                    # print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(
                    #    face_distance < 0.5))
                    if (face_distance < 0.4):
                        # print(format(face_distance, '2f'))
                        distance_same_face = True"""
                # print(matches)
                best_match_index = np.argmin(face_distances)
                """print(best_match_index)
                print(face_distances)
                print(matches[best_match_index])"""
                if matches[best_match_index]:  # and distance_same_face:
                    name_id = self.known_face_code[best_match_index]
                    # print(name_id)
                    preson_name = self.labels_name.get(int(name_id))
                    # list_p = {name_id: preson_name}
                    list_p = {name_id: min(face_distances)}
                    list_p.update(self.list_name_show)
                    self.list_name_show = list_p

                    found_face.update({np.amin(face_distances): name_id})
                    face_names.append(preson_name)

                else:
                    found_face.update({random.randint(10, 100): 1000})  # set values to unkwon
                    face_names.append(preson_name)
            # print(found_face)
            # use for checking multiperson distances round and get minimum distance
            i = -1
            for value, id in found_face.items():
                i = i + 1
                if id != 1000:
                    ss = []
                    for v, ids in found_face.items():
                        if ids != 1000 and id == ids:
                            ss.append(v)
                    for v, ids in found_face.items():
                        if ids != 1000:
                            if id == ids and value == min(ss):
                                # face_names[i] = self.labels_name.get(int(ids)) + " - " + str(
                                #    (float("{:.2f}".format(value))))
                                vl = str(value)
                                face_names[i] = self.labels_name.get(int(ids)) + " - " + vl[:4]
                            elif id == ids and value != min(ss):
                                face_names[i] = 'ບໍ່ຮູ້ຈັກຄົນນີ້.!'
            # end checking
            for (top, right, bottom, left), name in zip(self.face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                if name != 'ບໍ່ຮູ້ຈັກຄົນນີ້.!':
                    cv2.rectangle(frame, (left, top), (right, bottom), (3, 128, 37), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (3, 128, 37), cv2.FILLED)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                label = name
                tex_color = '#FFFFFF'
                font_size = 20
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

    def SetParameters(self, generate_camera_id, number_of_times, number_jitters, model_name):
        self.generate_camera_id = generate_camera_id
        self.webcam_id = generate_camera_id
        self.number_of_times = int(number_of_times)
        self.number_jitters = int(number_jitters)
        self.model_name = model_name.lower()
