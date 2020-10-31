from models.db import db


class Districts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dis_code = db.Column(db.String(255))
    dis_name = db.Column(db.String(255))
    dis_name_la = db.Column(db.String(255))
    provinces_id = db.Column(db.Integer)


def ListDistrictBy(provice_id):
    models = Districts.query.filter_by(
        provinces_id=provice_id
    ).all()
    district_list = [('', '=== ເລຶອກ ເມຶອງ ===')]
    if models:
        for model in models:
            data = (model.id, model.dis_name_la)
            district_list.append(data)
    return district_list
