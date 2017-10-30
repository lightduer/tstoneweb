from db.main import db


class UrlResource(db.Model):

    __tablename__ = 'url_resource'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(1024))
    method = db.Column(db.String(120))
    description = db.Column(db.String(120))

    def __init__(self, endpoint, method):
        self.endpoint = endpoint
        self.method = method


class UrlResourceManager(object):
    pass