from models.db import db


class Provinces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pro_code = db.Column(db.String(255))
    pro_name = db.Column(db.String(255))
    pro_name_la = db.Column(db.String(255))

def ListProvince():
    models = Provinces.query.all()
    proivce_list = [('','=== ເລຶອກ ແຂວງ ===')]
    if models:
        for model in models:
            data = (model.id, model.pro_name_la)
            proivce_list.append(data)
    return proivce_list