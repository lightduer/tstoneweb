import wtforms
from flask import Blueprint
from flask_restful import Api
from common.rest_method import Segment, MyResource

test1 = Blueprint("test_case1", __name__, url_prefix='/test_case1')
api = Api(test1)


class TestWelcome(MyResource):
    id = Segment(['DELETE', 'POST', 'PUT'], wtforms.StringField, default='', validator=[])

    def get(self):
        return 'Welcome to my test1 restful-blueprint'

api.add_resource(TestWelcome, '/welcome')

