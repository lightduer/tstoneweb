from flask import Blueprint
from flask_restful import Api
from common.valid_check import MyResource

user_view = Blueprint("user_view", __name__, url_prefix='/user')
api = Api(user_view)


class LoginView(MyResource):
    def get(self):
        return  '''
        <html>

            <head>

                <meta charset="utf-8" />

                <title>Flask - Test</title>

            </head>

            <body>

                <form action="/" method="post">
                    姓名：
                    <input type="text" name="username">
                    <input type="text" name="pw">
                    <input type="submit" value="Submit" />
                </form>

            </body>

        </html>
        '''

    def post(self):
        pass


api.add_resource(LoginView, '/login')
api.error_router = MyResource.error_router