from models.db import db


class Districts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dis_code = db.Column(db.String(255))
    dis_name = db.Column(db.String(255))
    dis_name_la = db.Column(db.String(255))
    provinces_id = db.Column(db.Integer)
