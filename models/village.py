from models.db import db;


class Villages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vill_code = db.Column(db.String(255))
    vill_name = db.Column(db.String(255))
    vill_name_la = db.Column(db.String(255))
    districts_id = db.Column(db.Integer)
    provinces_id = db.Column(db.Integer)
