# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, redirect
from flask_restful import Api, Resource

user_view = Blueprint("user_view", __name__, url_prefix='/user')
api = Api(user_view)


# @user_view.route('/login3')
# def login_view1():
#     return redirect(url_for('static', filename='login.html'))


class LoginView(Resource):

    def get(self):
        return redirect(url_for('static', filename='login.html'))

    def post(self):
        return 111


api.add_resource(LoginView, '/login')
