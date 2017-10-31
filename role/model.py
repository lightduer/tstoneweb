from db.main import db


class EndpointResource(db.Model):

    __tablename__ = 'endpoint_resource'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(1024))
    description = db.Column(db.String(120))

    def __init__(self, endpoint, desc):
        self.endpoint = endpoint
        self.description = desc


class WebItemResource(db.Model):
    __tablename__ = 'webitem_resource'

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(64))
    item_id = db.Column(db.String(120))
    item_name = db.Column(db.String(120))
    description = db.Column(db.String(120))

    def __init__(self, item_type, item_id, item_name, desc):
        self.item_type = item_type
        self.item_id = item_id
        self.item_name = item_name
        self.description = desc


# class DataResource(db.Model):
#     pass


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.Integer, nullable=False)
    role_name = db.Column(db.String(32), unique=True)
    desc = db.Column(db.String(255))

    def __init__(self, role_type, role_name, desc):
        self.role_type = role_type
        self.role_name = role_name
        self.desc = desc
