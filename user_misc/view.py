# -*- coding: utf-8 -*-
import wtforms
from flask import Blueprint
from flask_restful import Api
from wtforms import validators

from common.app_object import BaseObject, Segment

user_misc = Blueprint("user_misc", __name__, url_prefix='/um')
api = Api(user_misc)


@user_misc.route('/login')
def login():
    return "login"


@user_misc.route('/logout')
def logout():
    pass


@user_misc.route('/reset_pw')
def reset_pw():
    pass


@user_misc.route('/verify_code')
def verify_code():
    pass


class UserInfo(BaseObject):
    def get(self, user_id):
        # 获取用户信息
        return user_id

    def put(self, user_id):
        # 修改用户信息
        pass


class UserInfoList(BaseObject):

    name = Segment(['POST'], wtforms.StringField, default='', validator=[validators.Length(min=6, max=25)])
    email = Segment(['POST'], wtforms.StringField, default='', validator=[])
    password = Segment(['POST'], wtforms.PasswordField, default='', validator=[])

    def get(self):
        # 获取用户信息
        return "get"

    def post(self):
        # 创建用户信息
        pass


api.add_resource(UserInfoList, '/users')
api.add_resource(UserInfo, '/users/<user_id>')
