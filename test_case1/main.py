from flask import Blueprint
from flask_restful import Api, Resource

test1 = Blueprint("test_case1", __name__, url_prefix='/test_case1')
api = Api(test1)


class TestWelcome(Resource):
    def get(self):
        return 'Welcome to my test1 restful-blueprint'

api.add_resource(TestWelcome, '/welcome')

