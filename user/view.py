from flask import Blueprint
from flask_restful import Api
from common.valid_check import MyResource

user_view = Blueprint("user_view", __name__, url_prefix='/user')
api = Api(user_view)


class LoginView(MyResource):
    def get(self):
        return 'Welcome to my test2 restful-blueprint'


api.add_resource(LoginView, '/login')
api.error_router = MyResource.error_router