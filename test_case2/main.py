from flask import Blueprint
from flask_restful import Api
from common.wrapper_class import MyResource

test2 = Blueprint("test_case2", __name__, url_prefix='/test_case2')
api = Api(test2)


class TestWelcome(MyResource):
    def get(self):
        return 'Welcome to my test2 restful-blueprint'

api.add_resource(TestWelcome, '/welcome')
api.error_router = MyResource.error_router

