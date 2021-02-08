from models.db import db;
from datetime import datetime


class ListFound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.String(255))
    camera_id = db.Column(db.String(255))
    date_time = db.Column(db.DateTime)
    distace = db.Column(db.String(255))


def SaveFound(person_id, generate_camera_id, distace_value):
    found = ListFound()
    found.person_id = person_id,
    found.camera_id = generate_camera_id
    found.date_time = datetime.today()
    found.distace = distace_value
    db.session.add(found)
    db.session.commit()
