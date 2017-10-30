# -*- coding: utf-8 -*-
import wtforms
from flask import Blueprint, url_for, redirect
from flask_restful import Api
from common.wrapper_resource import Segment
from common.wrapper_resource import MyResource

user_view = Blueprint("user_view", __name__, url_prefix='/user')
api = Api(user_view)


# @user_view.route('/login3')
# def login_view1():
#     return redirect(url_for('static', filename='login.html'))


class LoginView(MyResource):

    username = Segment(['POST'], wtforms.StringField, default='', validator=[])
    pw = Segment(['POST'], wtforms.PasswordField, default='', validator=[])

    def get(self):
        return redirect(url_for('static', filename='login.html'))

    def post(self, username, pw):
        return 111


api.add_resource(LoginView, '/login')
api.error_router = MyResource.error_router