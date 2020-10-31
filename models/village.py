from models.db import db;


class Villages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vill_code = db.Column(db.String(255))
    vill_name = db.Column(db.String(255))
    vill_name_la = db.Column(db.String(255))
    districts_id = db.Column(db.Integer)
    provinces_id = db.Column(db.Integer)


def ListVillageBy(district_id):
    models = Villages.query.filter_by(
        districts_id=district_id
    ).all()
    village_list = [('', '=== ເລຶອກ ບ້ານ ===')]
    if models:
        for model in models:
            data = (model.id, model.vill_name_la)
            village_list.append(data)
    return village_list
