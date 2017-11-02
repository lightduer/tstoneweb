from db_model import db


class EndpointResource(db.Model):

    __tablename__ = 'endpoint_resource'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(1024))
    endpoint = db.Column(db.String(1024))
    description = db.Column(db.String(120))

    def __init__(self,key_id=None, uuid='', endpoint='', desc=''):
        self.id = key_id
        self.uuid = uuid
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
    # role_type = db.Column(db.Integer, nullable=False)
    role_name = db.Column(db.String(32))
    desc = db.Column(db.String(255))

    def __init__(self, role_name, desc):
        self.role_name = role_name
        self.desc = desc


class RoleEndpoint(db.Model):
    __tablename__ = 'role_endpoint'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    resource_id = db.Column(db.Integer)
    method = db.Column(db.String(32))
    desc = db.Column(db.String(255))

    def __init__(self, key_id=None, role_id=0, resource_id=0, method='GET', desc=''):
        self.id = key_id
        self.role_id = role_id
        self.resource_id = resource_id
        self.method = method
        self.desc = desc


