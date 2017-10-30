from db.main import db


class EndpointResource(db.Model):

    __tablename__ = 'endpoint_resource'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(1024))
    method = db.Column(db.String(120))
    description = db.Column(db.String(120))

    def __init__(self, endpoint, method, desc):
        self.endpoint = endpoint
        self.method = method
        self.description = desc