from flask import Blueprint
from flask_restful import Api, Resource

test2 = Blueprint("test_case2", __name__, url_prefix='/test_case2')
api = Api(test2)


class TestWelcome(Resource):
    def get(self):
        return 'Welcome to my test2 restful-blueprint'


api.add_resource(TestWelcome, '/welcome')


