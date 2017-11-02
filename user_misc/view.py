# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource

user_misc = Blueprint("user_misc", __name__, url_prefix='/user')
api = Api(user_misc)


@user_misc.route('/login')
def login():
    pass


@user_misc.route('/logout')
def logout():
    pass


@user_misc.route('/resetpw')
def reset_password():
    pass


class UserMisc(Resource):
    def get(self):
        # 获取用户信息
        pass

    def post(self):
        # 创建一个用户
        pass

    def put(self):
        # 修改用户信息
        pass


api.add_resource(UserMisc, '/user')
